from app.memory.memory import Memory, Message

def test_memory_add_get():
    memory = Memory()
    session_id = "sess_1"
    msg = Message(role="user", content="Hello")
    
    memory.add_message(session_id, msg)
    history = memory.get_history(session_id)
    
    assert len(history) == 1
    assert history[0].content == "Hello"

def test_memory_clear():
    memory = Memory()
    session_id = "sess_1"
    memory.add_message(session_id, Message(role="user", content="Hi"))
    
    memory.clear_history(session_id)
    assert len(memory.get_history(session_id)) == 0

def test_context_window():
    memory = Memory()
    session_id = "sess_1"
    for i in range(15):
        memory.add_message(session_id, Message(role="user", content=f"Msg {i}"))
        
    window = memory.get_context_window(session_id, limit=5)
    assert len(window) == 5
    assert window[-1].content == "Msg 14"
