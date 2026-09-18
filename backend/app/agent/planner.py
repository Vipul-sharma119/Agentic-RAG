from typing import List
from app.agent.state import AgentState
from app.llm.groq_client import get_groq_client
import logging
import json

from app.core.prompts import PLANNER_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self):
        self.llm = get_groq_client()
        self.system_prompt = PLANNER_SYSTEM_PROMPT

    async def create_plan(self, state: AgentState) -> List[str]:
        """
        Generates a plan based on the current state.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Query: {state.query}\nHistory: {state.history}"}
        ]
        
        try:
            response = self.llm.chat_completion(
                messages, 
                temperature=0.0,
                max_tokens=512
            )
            content = response.choices[0].message.content
            
            # Extract JSON from response
            json_str = content.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            start = json_str.find('{')
            end = json_str.rfind('}')
            if start != -1 and end != -1:
                json_str = json_str[start:end+1]
            
            plan_data = json.loads(json_str)
            steps = plan_data.get("steps", [])
            logger.info(f"Generated plan with {len(steps)} steps.")
            return steps
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            # Fallback simple plan
            return ["Retrieve relevant information", "Answer the query"]

def get_planner() -> Planner:
    return Planner()
