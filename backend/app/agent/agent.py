from typing import Dict, Any, List, Optional, AsyncGenerator
from app.agent.state import AgentState, Message
from app.agent.planner import get_planner
from app.agent.tools import get_tools, BaseTool
from app.llm.groq_client import get_groq_client
import logging
import json
import time
from app.core.prompts import AGENT_DECISION_PROMPT, RESPONSE_STYLE_PROMPT

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self):
        self.planner = get_planner()
        self.tools = {t.name: t for t in get_tools()}
        self.llm = get_groq_client()
        self._tool_schemas = [t.to_schema() for t in self.tools.values()]
        
    async def run(self, query: str, session_id: str = "default", prior_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Main agent loop with optional session history (non-streaming).
        """
        state = AgentState(query=query)
        
        if prior_history:
            for msg in prior_history[-6:]:
                state.history.append(Message(role=msg["role"], content=msg["content"]))
        
        logger.info(f"Starting agent run for query: {query} (session: {session_id})")
        
        plan_steps = await self.planner.create_plan(state)
        state.plan = plan_steps
        
        max_steps = 10
        collected_context = []
        
        for step_num in range(max_steps):
            action = await self._decide_next_action(state)
            
            if action["type"] == "finish":
                state.scratchpad["raw_answer"] = action.get("content", "")
                logger.info("Agent tool-calling loop finished.")
                break
                
            if action["type"] == "tool_use":
                tool_name = action["tool"]
                tool_args = action.get("args", {})
                
                if tool_name in self.tools:
                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                    result = self.tools[tool_name].run(**tool_args)
                    
                    state.history.append(Message(role="assistant", content=f"Tool Request: {tool_name}({json.dumps(tool_args)})"))
                    state.history.append(Message(role="tool", content=str(result)))
                    collected_context.append(str(result))
                else:
                    state.history.append(Message(role="system", content=f"Tool {tool_name} not found."))
            
            if action["type"] == "message":
                 state.history.append(Message(role="assistant", content=action["content"]))

        state.final_answer = await self._synthesize_response(state, collected_context)

        return {
            "query": state.query,
            "answer": state.final_answer,
            "plan": state.plan,
            "history": [m.dict() for m in state.history]
        }

    async def run_stream(self, query: str, session_id: str = "default", prior_history: List[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming agent loop — yields SSE events at each pipeline stage.
        """
        run_start = time.time()
        state = AgentState(query=query)
        
        if prior_history:
            for msg in prior_history[-6:]:
                state.history.append(Message(role=msg["role"], content=msg["content"]))
        
        logger.info(f"Starting streaming agent run for query: {query} (session: {session_id})")
        
        # ── Stage 1: Planning ──
        yield {"event": "status", "data": {"step": "planning", "message": "Generating execution plan..."}}
        
        t0 = time.time()
        plan_steps = await self.planner.create_plan(state)
        state.plan = plan_steps
        plan_ms = int((time.time() - t0) * 1000)
        
        yield {"event": "plan", "data": {"steps": plan_steps, "elapsed_ms": plan_ms}}
        
        # ── Stage 2: Tool-calling loop ──
        max_steps = 10
        collected_context = []
        
        for step_num in range(max_steps):
            yield {"event": "status", "data": {"step": "deciding", "message": f"Deciding next action (step {step_num + 1})..."}}
            
            action = await self._decide_next_action(state)
            
            if action["type"] == "finish":
                state.scratchpad["raw_answer"] = action.get("content", "")
                logger.info("Agent tool-calling loop finished.")
                break
                
            if action["type"] == "tool_use":
                tool_name = action["tool"]
                tool_args = action.get("args", {})
                
                yield {"event": "tool_call", "data": {"tool": tool_name, "args": tool_args}}
                
                if tool_name in self.tools:
                    t1 = time.time()
                    yield {"event": "status", "data": {"step": "executing_tool", "message": f"Running {tool_name}..."}}
                    
                    result = self.tools[tool_name].run(**tool_args)
                    tool_ms = int((time.time() - t1) * 1000)
                    
                    state.history.append(Message(role="assistant", content=f"Tool Request: {tool_name}({json.dumps(tool_args)})"))
                    state.history.append(Message(role="tool", content=str(result)))
                    collected_context.append(str(result))
                    
                    yield {"event": "tool_result", "data": {
                        "tool": tool_name,
                        "result": str(result)[:500],  # Truncate for SSE
                        "elapsed_ms": tool_ms,
                    }}
                else:
                    state.history.append(Message(role="system", content=f"Tool {tool_name} not found."))
                    yield {"event": "error", "data": {"message": f"Tool {tool_name} not found."}}
            
            if action["type"] == "message":
                 state.history.append(Message(role="assistant", content=action["content"]))

        # ── Stage 3: Streaming synthesis ──
        yield {"event": "status", "data": {"step": "generating", "message": "Generating response..."}}
        
        full_answer = ""
        async for token_event in self._synthesize_response_stream(state, collected_context):
            full_answer += token_event.get("content", "")
            yield {"event": "token", "data": token_event}
        
        state.final_answer = full_answer
        total_ms = int((time.time() - run_start) * 1000)
        
        yield {"event": "done", "data": {
            "answer": full_answer,
            "plan": state.plan,
            "history": [m.dict() for m in state.history],
            "total_ms": total_ms,
        }}

    async def _decide_next_action(self, state: AgentState) -> Dict[str, Any]:
        """
        Uses Groq's native tool calling to decide the next action.
        """
        prompt = AGENT_DECISION_PROMPT.format(
            query=state.query,
            plan=state.plan,
            history=[m.dict() for m in state.history[-8:]],
            tools_desc="Available as native tool calls."
        )
        
        messages = [{"role": "system", "content": prompt}]
        
        try:
            response = self.llm.chat_completion(
                messages,
                temperature=0.3,
                max_tokens=1024,
                tools=self._tool_schemas,
                tool_choice="auto"
            )
            
            choice = response.choices[0]
            message = choice.message
            
            if message.tool_calls and len(message.tool_calls) > 0:
                tool_call = message.tool_calls[0]
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {"query": state.query}
                
                logger.info(f"Native tool call: {tool_name}({tool_args})")
                
                if tool_name == "final_answer":
                    return {"type": "finish", "content": tool_args.get("answer", "")}
                
                return {"type": "tool_use", "tool": tool_name, "args": tool_args}
            
            content = message.content or ""
            
            if content.strip():
                try:
                    json_str = content.strip()
                    if "```json" in json_str:
                        json_str = json_str.split("```json")[1].split("```")[0].strip()
                    elif "```" in json_str:
                        json_str = json_str.split("```")[1].split("```")[0].strip()
                    
                    start = json_str.find('{')
                    end = json_str.rfind('}')
                    if start != -1 and end != -1:
                        json_str = json_str[start:end+1]
                        parsed = json.loads(json_str)
                        if "type" in parsed:
                            return parsed
                except (json.JSONDecodeError, KeyError):
                    pass
                
                return {"type": "finish", "content": content}
            
            return {"type": "finish", "content": "I could not generate a response."}
            
        except Exception as e:
            logger.error(f"Decision failed: {e}")
            return {"type": "finish", "content": "I encountered an error and cannot proceed."}

    async def _synthesize_response(self, state: AgentState, collected_context: List[str]) -> str:
        """
        Final synthesis step (non-streaming).
        """
        context_text = "\n\n---\n\n".join(collected_context) if collected_context else "No documents were retrieved."
        
        history_text = ""
        for msg in state.history:
            if msg.role in ("user", "assistant") and not msg.content.startswith("Tool Request:"):
                history_text += f"{msg.role}: {msg.content}\n"
        
        prompt = RESPONSE_STYLE_PROMPT.format(
            query=state.query,
            context=context_text,
            history=history_text or "No prior conversation."
        )
        
        try:
            response = self.llm.chat_completion(
                [{"role": "system", "content": prompt}],
                temperature=0.5,
                max_tokens=2048,
            )
            
            answer = response.choices[0].message.content
            if answer and answer.strip():
                return answer.strip()
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
        
        return state.scratchpad.get("raw_answer", "I was unable to formulate a response.")

    async def _synthesize_response_stream(self, state: AgentState, collected_context: List[str]) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming synthesis — yields token chunks as they arrive from Groq.
        """
        context_text = "\n\n---\n\n".join(collected_context) if collected_context else "No documents were retrieved."
        
        history_text = ""
        for msg in state.history:
            if msg.role in ("user", "assistant") and not msg.content.startswith("Tool Request:"):
                history_text += f"{msg.role}: {msg.content}\n"
        
        prompt = RESPONSE_STYLE_PROMPT.format(
            query=state.query,
            context=context_text,
            history=history_text or "No prior conversation."
        )
        
        try:
            stream = self.llm.chat_completion_stream(
                [{"role": "system", "content": prompt}],
                temperature=0.5,
                max_tokens=2048,
            )
            
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        yield {"content": delta.content}
                        
        except Exception as e:
            logger.error(f"Streaming synthesis failed: {e}")
            raw = state.scratchpad.get("raw_answer", "I was unable to formulate a response.")
            yield {"content": raw}

def get_agent() -> Agent:
    return Agent()
