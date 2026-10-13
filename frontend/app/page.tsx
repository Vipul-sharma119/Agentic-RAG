"use client";

import { Activity, ArrowRight, BookOpen, CheckCircle2, ChevronDown, ChevronLeft, ChevronRight, CircleHelp, Command, FileText, FileUp, FlaskConical, LoaderCircle, Menu, MessageSquare, Moon, MoreHorizontal, Plus, Search, Send, Settings2, ShieldCheck, Sparkles, Sun, UploadCloud, X, Zap } from "lucide-react";
import { ChangeEvent, DragEvent, FormEvent, useCallback, useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const API = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");
type Message = { id: string; role: "user" | "assistant"; content: string; streaming?: boolean };
type Session = { session_id: string; preview: string; updated_at?: string };
type EventData = { event: string; data: Record<string, unknown> };
const uid = () => typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : "session-" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
function errorText(data: unknown) {
  if (typeof data === "string") return data;
  if (data && typeof data === "object") {
    const d = data as Record<string, unknown>;
    if (typeof d.detail === "string") return d.detail;
    if (typeof d.message === "string") return d.message;
  }
  return "Request failed. Check the backend connection and try again.";
}
async function parseSSE(response: Response, onEvent: (event: EventData) => void, signal: AbortSignal) {
  if (!response.body) throw new Error("The server did not return a readable stream.");
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    if (signal.aborted) { await reader.cancel(); return; }
    const part = await reader.read();
    if (part.done) break;
    buffer += decoder.decode(part.value, { stream: true }).replace(/\r\n/g, "\n");
    let index = buffer.indexOf("\n\n");
    while (index >= 0) {
      const block = buffer.slice(0, index);
      buffer = buffer.slice(index + 2);
      let event = "message";
      const lines: string[] = [];
      block.split("\n").forEach((line) => {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        if (line.startsWith("data:")) lines.push(line.slice(5).trimStart());
      });
      if (lines.length) {
        try { onEvent({ event, data: JSON.parse(lines.join("\n")) as Record<string, unknown> }); }
        catch { onEvent({ event, data: { message: lines.join("\n") } }); }
      }
      index = buffer.indexOf("\n\n");
    }
  }
}
function dateLabel(value?: string) {
  if (!value) return "";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? "" : d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export default function Home() {
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [apiState, setApiState] = useState("checking");
  const [theme, setTheme] = useState("dark");
  const [sidebar, setSidebar] = useState(true);
  const [showUpload, setShowUpload] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [notice, setNotice] = useState("");
  const [plan, setPlan] = useState<string[]>([]);
  const [activity, setActivity] = useState<string[]>([]);
  const [showActivity, setShowActivity] = useState(true);
  const [filter, setFilter] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    const savedTheme = localStorage.getItem("agentic-theme");
    if (savedTheme === "light" || savedTheme === "dark") setTheme(savedTheme);
    const id = localStorage.getItem("agentic-session") || uid();
    localStorage.setItem("agentic-session", id);
    setSessionId(id);
  }, []);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("agentic-theme", theme);
  }, [theme]);
  const checkApi = useCallback(async () => {
    try { const r = await fetch(API + "/health", { cache: "no-store" }); setApiState(r.ok ? "online" : "offline"); }
    catch { setApiState("offline"); }
  }, []);
  const refreshSessions = useCallback(async () => {
    try {
      const r = await fetch(API + "/api/v1/sessions/", { cache: "no-store" });
      if (r.ok) { const data = await r.json() as Session[]; setSessions(Array.isArray(data) ? data : []); }
    } catch { /* Session history is optional; chat itself still works. */ }
  }, []);
  useEffect(() => { void checkApi(); void refreshSessions(); }, [checkApi, refreshSessions]);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" }); }, [messages, activity]);
  useEffect(() => () => abortRef.current?.abort(), []);

  const newChat = () => {
    if (busy) return;
    const id = uid(); setSessionId(id); localStorage.setItem("agentic-session", id);
    setMessages([]); setPlan([]); setActivity([]); setNotice(""); setInput(""); setShowActivity(true);
  };
  const openSession = async (id: string) => {
    if (busy) return;
    setSessionId(id); localStorage.setItem("agentic-session", id); setNotice(""); setPlan([]); setActivity([]);
    try {
      const r = await fetch(API + "/api/v1/sessions/" + encodeURIComponent(id));
      if (!r.ok) throw new Error("This session is no longer available on the backend.");
      const data = await r.json() as { messages?: { role: string; content: string }[] };
      setMessages((data.messages || []).filter((m) => m.role === "user" || m.role === "assistant").map((m, i) => ({ id: id + "-" + i, role: m.role as "user" | "assistant", content: m.content })));
    } catch (e) { setMessages([]); setNotice(e instanceof Error ? e.message : "Could not open this session."); }
  };

  const send = async (event?: FormEvent, preset?: string) => {
    event?.preventDefault();
    const query = (preset !== undefined ? preset : input).trim();
    if (!query || busy || !sessionId) return;
    setInput(""); setNotice(""); setPlan([]); setActivity([]); setShowActivity(true);
    const assistantId = uid();
    setMessages((prev) => [...prev, { id: uid(), role: "user", content: query }, { id: assistantId, role: "assistant", content: "", streaming: true }]);
    setBusy(true);
    const controller = new AbortController(); abortRef.current = controller;
    const log = (line: string) => setActivity((prev) => [...prev, line].slice(-12));
    try {
      const r = await fetch(API + "/api/v1/chat/stream", {
        method: "POST", headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
        body: JSON.stringify({ query, session_id: sessionId }), signal: controller.signal,
      });
      if (!r.ok) {
        let detail: unknown;
        try { detail = await r.json(); } catch { detail = await r.text(); }
        throw new Error(errorText(detail));
      }
      await parseSSE(r, (item) => {
        const d = item.data;
        if (item.event === "status") log(typeof d.message === "string" ? d.message : "Agent is working…");
        else if (item.event === "plan") { setPlan(Array.isArray(d.steps) ? d.steps.map(String) : []); log("Execution plan ready"); }
        else if (item.event === "tool_call") log("Using tool: " + String(d.tool || "tool"));
        else if (item.event === "tool_result") log("Finished: " + String(d.tool || "tool"));
        else if (item.event === "token" && typeof d.content === "string") {
          const token = d.content;
          setMessages((prev) => prev.map((m) => m.id === assistantId ? { ...m, content: m.content + token } : m));
        } else if (item.event === "done") {
          const answer = typeof d.answer === "string" ? d.answer : "";
          setMessages((prev) => prev.map((m) => m.id === assistantId ? { ...m, content: answer || m.content, streaming: false } : m));
          log("Response complete");
        } else if (item.event === "error") throw new Error(typeof d.message === "string" ? d.message : "The agent reported an error.");
      }, controller.signal);
      setMessages((prev) => prev.map((m) => m.id === assistantId ? { ...m, streaming: false } : m));
      void refreshSessions(); void checkApi();
    } catch (e) {
      if (e instanceof Error && e.name === "AbortError") return;
      setNotice(e instanceof Error ? e.message : "Unable to reach the agent.");
      setMessages((prev) => prev.map((m) => m.id === assistantId ? { ...m, content: m.content || "I couldn't complete that request. Check the backend connection and try again.", streaming: false } : m));
      log("Run stopped");
    } finally { setBusy(false); abortRef.current = null; }
  };

  const upload = async (file?: File) => {
    if (!file || uploading) return;
    if (!/\.(pdf|txt)$/i.test(file.name)) { setNotice("Please choose a PDF or TXT file."); return; }
    setUploading(true); setNotice("");
    const form = new FormData(); form.append("file", file);
    try {
      const r = await fetch(API + "/api/v1/ingest/", { method: "POST", body: form });
      let data: Record<string, unknown> = {};
      try { data = await r.json() as Record<string, unknown>; } catch { /* use generic error */ }
      if (!r.ok) throw new Error(errorText(data));
      setNotice("Indexed " + String(data.filename || file.name) + " · " + String(data.chunks_processed ?? "—") + " chunks added to your knowledge base.");
      setShowUpload(false); void checkApi();
    } catch (e) { setNotice(e instanceof Error ? e.message : "Document upload failed."); }
    finally { setUploading(false); if (fileRef.current) fileRef.current.value = ""; }
  };
  const onFileChange = (e: ChangeEvent<HTMLInputElement>) => void upload(e.target.files?.[0]);
  const onDrop = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setDragging(false); void upload(e.dataTransfer.files?.[0]); };
  const visibleSessions = sessions.filter((s) => (s.preview || "").toLowerCase().includes(filter.toLowerCase()));

  return <main className="app-shell">
    <aside className={"sidebar " + (sidebar ? "sidebar-open" : "sidebar-closed")}>
      <div className="brand-row"><div className="brand-mark"><Sparkles size={19}/></div><div className="brand-copy"><span>agentic<span className="brand-accent">.</span></span><small>RESEARCH WORKSPACE</small></div><button className="icon-button sidebar-collapse" aria-label="Collapse sidebar" onClick={() => setSidebar(false)}><ChevronLeft size={17}/></button></div>
      <button className="new-chat-button" onClick={newChat} disabled={busy}><Plus size={17}/><span>New conversation</span><span className="shortcut">⌘ K</span></button>
      <button className="nav-item active" onClick={() => setShowUpload(false)}><MessageSquare size={17}/><span>Chat workspace</span><span className="nav-dot"/></button>
      <button className="nav-item" onClick={() => setShowUpload((v) => !v)}><BookOpen size={17}/><span>Knowledge library</span><span className="nav-count">PDF / TXT</span></button>
      <div className="sidebar-section"><div className="section-label"><span>RECENT CONVERSATIONS</span><button className="tiny-icon" aria-label="Refresh sessions" onClick={() => void refreshSessions()}><MoreHorizontal size={16}/></button></div>
        <div className="conversation-search"><Search size={14}/><input value={filter} onChange={(e) => setFilter(e.target.value)} placeholder="Find a conversation"/></div>
        <div className="conversation-list">{visibleSessions.length ? visibleSessions.map((s) => <button key={s.session_id} className={"conversation-item " + (sessionId === s.session_id ? "selected" : "")} onClick={() => void openSession(s.session_id)}><MessageSquare size={15}/><span className="conversation-text">{s.preview || "New conversation"}</span><span className="conversation-date">{dateLabel(s.updated_at)}</span></button>) : <div className="empty-history">{filter ? "No matches found" : "Your conversations will appear here."}</div>}</div>
      </div>
      <div className="sidebar-spacer"/>
      <div className="sidebar-knowledge"><div className="knowledge-icon"><FlaskConical size={17}/></div><div><strong>Your knowledge base</strong><p>Ask questions grounded in your own documents.</p></div><button aria-label="Upload a document" onClick={() => setShowUpload(true)}><Plus size={16}/></button></div>
      <div className="sidebar-footer"><div className="avatar">V</div><div className="profile-copy"><strong>Personal workspace</strong><span>Local development</span></div><button className="icon-button" aria-label="Settings" onClick={() => setNotice("API endpoint: " + API)}><Settings2 size={17}/></button></div>
    </aside>
    <section className="main-panel">
      <header className="topbar"><div className="topbar-left">{!sidebar && <button className="icon-button" aria-label="Open sidebar" onClick={() => setSidebar(true)}><Menu size={19}/></button>}<div className="breadcrumb"><span>Workspace</span><ChevronRight size={14}/><strong>Chat</strong></div></div>
        <div className="topbar-right"><div className={"connection-status " + apiState}><span className="status-indicator"/>{apiState === "online" ? "API connected" : apiState === "checking" ? "Connecting…" : "API offline"}</div><span className="topbar-divider"/><button className="icon-button theme-toggle" aria-label="Toggle theme" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>{theme === "dark" ? <Sun size={17}/> : <Moon size={17}/>}</button><button className="help-button" onClick={() => setNotice("Upload a PDF or TXT file, then ask a question. The agent plans steps, retrieves relevant passages, and streams its answer.")}><CircleHelp size={16}/><span>Help</span></button></div>
      </header>
      <div className="workspace-scroll"><div className="workspace-content">
        {showUpload && <section className="upload-panel"><div className="upload-panel-heading"><div><span className="eyebrow">KNOWLEDGE LIBRARY</span><h2>Add documents</h2><p>Files are chunked, embedded and indexed for retrieval.</p></div><button className="icon-button" onClick={() => setShowUpload(false)} aria-label="Close upload"><X size={18}/></button></div>
          <div className={"drop-zone " + (dragging ? "dragging" : "") + (uploading ? " is-uploading" : "")} onDragOver={(e) => { e.preventDefault(); setDragging(true); }} onDragLeave={() => setDragging(false)} onDrop={onDrop}>{uploading ? <LoaderCircle className="spin" size={27}/> : <UploadCloud size={28}/>}<strong>{uploading ? "Indexing your document…" : "Drop a document here"}</strong><span>{uploading ? "Keep this tab open while the API processes the file." : "PDF and plain-text files"}</span><button type="button" className="secondary-button" onClick={() => fileRef.current?.click()} disabled={uploading}><FileUp size={16}/> Choose file</button><input ref={fileRef} type="file" accept=".pdf,.txt,application/pdf,text/plain" hidden onChange={onFileChange}/></div>
        </section>}
        {messages.length === 0 ? <div className="welcome-view">
          <div className="welcome-pill"><span className="pulse-dot"/> YOUR DOCUMENTS, REASONED THROUGH <ArrowRight size={13}/></div>
          <div className="hero-symbol"><div className="hero-symbol-inner"><Sparkles size={31} strokeWidth={1.5}/></div><span className="orbit orbit-one"/><span className="orbit orbit-two"/></div>
          <h1>Research at the<br/><span>speed of thought.</span></h1>
          <p className="hero-description">An AI research partner that plans, retrieves and reasons across your documents — with answers from your own knowledge base.</p>
          <div className="capability-row"><div><span className="capability-icon purple"><Zap size={16}/></span><strong>Agentic reasoning</strong><small>Multi-step problem solving</small></div><div><span className="capability-icon blue"><Search size={16}/></span><strong>Grounded retrieval</strong><small>Search with reranking</small></div><div><span className="capability-icon green"><Activity size={16}/></span><strong>Live execution</strong><small>Follow each agent step</small></div></div>
          <div className="suggestion-heading"><span>GET STARTED</span><span>TRY A PROMPT <ArrowRight size={12}/></span></div>
          <div className="suggestion-grid">
            <button onClick={() => void send(undefined, "Summarize the key findings in my documents.")}><span className="suggestion-icon lilac"><FileText size={17}/></span><span><strong>Summarize my documents</strong><small>Pull out the most important ideas</small></span><ArrowRight size={16}/></button>
            <button onClick={() => void send(undefined, "Compare the main arguments and evidence across my documents.")}><span className="suggestion-icon cyan"><Activity size={17}/></span><span><strong>Compare ideas and evidence</strong><small>Connect details across sources</small></span><ArrowRight size={16}/></button>
            <button onClick={() => void send(undefined, "What calculations or quantitative insights can you derive from my documents?")}><span className="suggestion-icon amber"><FlaskConical size={17}/></span><span><strong>Find quantitative insights</strong><small>Reason through numbers and facts</small></span><ArrowRight size={16}/></button>
            <button onClick={() => { setShowUpload(true); setNotice(""); }}><span className="suggestion-icon mint"><UploadCloud size={17}/></span><span><strong>Start with a document</strong><small>Upload a PDF or text file first</small></span><ArrowRight size={16}/></button>
          </div><div className="welcome-footnote"><ShieldCheck size={14}/> Answers may need verification against your source documents.</div>
        </div> : <div className="chat-view">
          <div className="chat-heading"><div><span className="eyebrow">YOUR RESEARCH SESSION</span><h1>Let's work through it.</h1></div><button className="secondary-button compact" onClick={() => setShowActivity((v) => !v)}><Activity size={15}/> Agent activity <ChevronDown size={14} className={showActivity ? "rotate" : ""}/></button></div>
          {showActivity && (plan.length > 0 || activity.length > 0) && <div className="activity-card"><div className="activity-title"><span className="activity-live"><span/> LIVE RUN</span><strong>Agent execution</strong><button onClick={() => setShowActivity(false)} aria-label="Hide agent activity"><X size={15}/></button></div>
            {plan.length > 0 && <div className="plan-list">{plan.map((step, i) => <div className="plan-step" key={i + "-" + step}><span>{String(i + 1).padStart(2, "0")}</span><p>{step}</p><CheckCircle2 size={15}/></div>)}</div>}
            {activity.length > 0 && <div className="activity-log">{activity.slice(-5).map((line, i) => <div key={line + "-" + i}><span className={"log-dot " + (i === activity.slice(-5).length - 1 && busy ? "live" : "")}/>{line}</div>)}</div>}
          </div>}
          <div className="messages-list">{messages.map((m) => <article key={m.id} className={"message-row " + m.role}><div className={"message-avatar " + m.role}>{m.role === "assistant" ? <Sparkles size={17}/> : "V"}</div><div className="message-main"><div className="message-meta"><strong>{m.role === "assistant" ? "Agentic" : "You"}</strong>{m.role === "assistant" && <span className="assistant-badge">AI RESEARCHER</span>}{m.streaming && <span className="streaming-label"><span/> generating</span>}</div><div className="message-content">{m.content ? <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown> : m.streaming ? <div className="thinking-indicator"><span/><span/><span/><em>Thinking through your question…</em></div> : null}{m.streaming && m.content && <span className="stream-cursor"/>}</div></div></article>)}<div ref={bottomRef}/></div>
        </div>}
        {notice && <div className={"notice " + (/failed|couldn't|offline|error/i.test(notice) ? "notice-error" : "")} role="status"><span>{notice}</span><button onClick={() => setNotice("")} aria-label="Dismiss message"><X size={15}/></button></div>}
      </div></div>
      <div className="composer-wrap"><form className="composer" onSubmit={(e) => void send(e)}>
        <div className="composer-tools"><button type="button" className={"composer-tool " + (showUpload ? "active" : "")} onClick={() => setShowUpload((v) => !v)} aria-label="Attach document"><Plus size={17}/></button><span className="composer-tool-label">Ask your knowledge base</span><span className="composer-model"><span/> GROQ · AGENT</span></div>
        <textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); void send(); } }} placeholder="Ask a question, connect ideas, or work through a problem…" rows={2} disabled={busy} aria-label="Message the agent"/>
        <div className="composer-bottom"><span><Command size={12}/> Enter to send <span className="key-separator">·</span> Shift + Enter for a new line</span><button type={busy ? "button" : "submit"} className={"send-button " + (input.trim() && !busy ? "ready" : "")} disabled={!busy && !input.trim()} onClick={busy ? () => abortRef.current?.abort() : undefined} aria-label={busy ? "Stop generating" : "Send message"}>{busy ? <><X size={16}/><span>Stop</span></> : <><Send size={15}/><span>Send</span></>}</button></div>
      </form><p className="composer-disclaimer">Agentic RAG can make mistakes. Verify important information against your source documents.</p></div>
    </section>
  </main>;
}
