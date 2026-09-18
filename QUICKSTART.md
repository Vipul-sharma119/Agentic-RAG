# 🚀 Quick Start Guide

Get your Agentic RAG system up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.10 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] Docker installed (for Qdrant)
- [ ] Groq API key ([Get it here](https://console.groq.com/))
- [ ] Hugging Face token ([Get it here](https://huggingface.co/settings/tokens))

## Step-by-Step Setup

### 1. Start Qdrant (Vector Database)

```bash
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant
```

Verify it's running: http://localhost:6333/dashboard

### 2. Backend Setup (5 commands)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Mac/Linux
```

**Edit `backend/.env`** with your API keys:
```env
GROQ_API_KEY=gsk_your_actual_groq_key_here
HF_TOKEN=hf_your_actual_huggingface_token_here
```

**Start the backend:**
```bash
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

### 3. Frontend Setup (4 commands)

Open a **new terminal** window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
copy .env.local.example .env.local  # Windows
# OR
cp .env.local.example .env.local    # Mac/Linux

# Start the frontend
npm run dev
```

✅ Frontend running at: http://localhost:3000

## First Steps

### 1. Ingest a Document

1. Open http://localhost:3000
2. Click **"Ingest"** in the navigation
3. Upload a PDF or TXT file
4. Wait for processing to complete

### 2. Start Chatting

1. Click **"Chat"** in the navigation
2. Type a question about your document
3. Watch the agent work:
   - 📋 Generate a plan
   - 🔍 Retrieve relevant information
   - 💬 Stream the response

### Example Questions

Try these queries:

```
"Summarize the main points from the document"
"What is mentioned about revenue in 2023?"
"Calculate 15% of the total mentioned"
"Explain the key findings"
```

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Make sure virtual environment is activated and dependencies are installed
  ```bash
  pip install -r requirements.txt
  ```

**Error**: `Connection refused to Qdrant`
- **Solution**: Make sure Qdrant is running
  ```bash
  docker ps  # Check if qdrant container is running
  docker start qdrant  # Start if stopped
  ```

**Error**: `Invalid API key`
- **Solution**: Check your `.env` file has correct API keys

### Frontend won't start

**Error**: `Cannot find module 'next'`
- **Solution**: Install dependencies
  ```bash
  npm install
  ```

**Error**: `Failed to fetch from backend`
- **Solution**: Make sure backend is running on http://localhost:8000

### Qdrant Issues

**Can't access Qdrant dashboard**
- **Solution**: Check Docker container
  ```bash
  docker ps
  docker logs qdrant
  ```

**Port 6333 already in use**
- **Solution**: Stop other Qdrant instances or change port in `.env`

## Verify Everything Works

### 1. Check Backend Health

Open: http://localhost:8000/docs

You should see the FastAPI Swagger documentation.

### 2. Check Frontend

Open: http://localhost:3000

You should see the chat interface.

### 3. Test the Flow

1. Upload a test document
2. Ask a question about it
3. See the agent retrieve and respond

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🎨 Explore the chat features (edit, retry, copy messages)
- 🔧 Customize prompts in `backend/app/core/prompts.py`
- 🛠️ Add custom tools in `backend/app/agent/tools.py`

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Review the API docs at http://localhost:8000/docs

---

**Happy chatting! 🤖✨**
