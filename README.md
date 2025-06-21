
# 🛠️ Internal IT Support Chatbot (Slack + RAG, Cohere, ChromaDB)

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A production-grade Retrieval-Augmented Generation (RAG) chatbot for instant, reliable IT support—right inside Slack, using your company's official PDF knowledge base.**

---

## 📖 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Slack App Setup](#slack-app-setup)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Extending](#extending)
- [Security](#security)
- [Interview/Resume Notes](#interviewresume-notes)
- [Credits](#credits)

---

## 📝 Overview

This project is a **Slack-integrated RAG chatbot** for internal IT support.  
Employees get instant, context-aware answers to IT questions, sourced only from official company PDF documentation, **without leaving Slack**.

- **No waiting for a helpdesk agent!**
- **No hallucinations—answers are always grounded in your company docs.**
- **Session memory** is maintained per Slack user for conversational support.

---

## 🏗️ Architecture

```
[Employee on Slack]
       |
    [Slack App/Bot]
       |
[FastAPI Backend (RAG)]
       |
[ChromaDB Vector Store]
       |
[Cohere (LLM/Embeddings)]
       |
[IT Knowledge PDFs]
```

**Flow:**  
1. Employee DMs the bot or mentions it in a channel.
2. Bot receives question and user ID, sends to FastAPI backend.
3. Backend retrieves relevant PDF chunks, runs Cohere LLM, tracks session history.
4. Bot responds in Slack with the answer and document sources.

---

## ✨ Features

- **Native Slack integration:** Employees use IT chatbot without switching tools.
- **Retrieval-Augmented Generation:** Combines vector search + LLM for factual answers.
- **PDF knowledge base:** All answers grounded in company documentation.
- **Session-aware:** Bot remembers user context and chat history.
- **Source referencing:** Every answer includes the document(s) and page(s) cited.
- **Secure:** No keys in code; secrets managed via environment variables.

---

## 📂 Project Structure

```
rag-it-support-chatbot/
├── app/
│   ├── ingest.py         # PDF ingestion & embedding
│   ├── rag_chain.py      # RAG chain logic
│   └── api.py            # FastAPI backend
├── slack_bot.py          # Slack bot event listener
├── requirements.txt      # All dependencies (add slack_bolt, slack_sdk)
├── README.md
├── data/                 # Company IT PDFs
└── memory_store/         # Session memory storage
```

---

## ⚙️ Setup

**Requirements:**  
- Python 3.9+  
- [Cohere API Key](https://dashboard.cohere.com/api-keys)  
- Slack workspace with permission to add custom apps  
- IT documentation as PDF in `/data`

---

### 1. Clone and Install

```sh
git clone https://github.com/your-org/rag-it-support-chatbot.git
cd rag-it-support-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment

```sh
# Set your Cohere API Key
export COHERE_API_KEY=your-cohere-api-key

# Optional: Set persistent vector store directory
export CHROMA_DB_DIR=your/path/to/vectorstore
```

### 3. Add IT PDFs

Put your company’s FAQ, policy, and troubleshooting PDFs in `data/`.

---

## 🤖 Slack App Setup

1. Go to [Slack API: Create an App](https://api.slack.com/apps) and create a new app.
2. Enable **Bots** and **Socket Mode**.
3. Add permissions:  
   - `chat:write`  
   - `app_mentions:read`  
   - `im:history`
4. Install app to your workspace.
5. Note your:
    - **Bot User OAuth Token** (`xoxb-...`)
    - **App Token** (`xapp-...` for Socket Mode)
6. Invite your bot to desired Slack channels.

---

## 🚦 Ingest Documents and Start Backend

### 1. Ingest PDFs

```sh
python app/ingest.py
```
*(Re-run this step whenever your PDFs change.)*

### 2. Start Backend API

```sh
uvicorn app.api:app --reload
```
*(Ensure this is running wherever the Slack bot will access it. Update `FASTAPI_URL` if needed.)*

---

## 🚀 Run Slack Bot

Set these environment variables in your terminal (or with a `.env` manager):

```sh
export SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxxxxx
export SLACK_APP_TOKEN=xapp-xxxxxxxxxxxxxxxx
export FASTAPI_URL=http://localhost:8000/ask # change if backend is remote/production
```

Then run:
```sh
python slack_bot.py
```

---

## 💬 Usage

- **Mention the bot in any Slack channel:**  
  ```
  @your-bot How do I reset my VPN password?
  ```
  The bot replies in a thread with the answer and sources.

- **DM the bot:**  
  Just type your question, and it replies in the DM.

- **Session memory:**  
  Each user's chat history is remembered using their Slack user ID.

---

## 🧠 How It Works

- **Employee types question** (channel mention or DM).
- **Bot receives event**, extracts text and Slack user ID.
- **Sends question + session_id** to FastAPI `/ask` endpoint.
- **Backend retrieves PDF chunks**, generates answer with Cohere LLM, tracks memory per user.
- **Bot replies** in Slack (thread or DM) with the answer and cited documents.

---

## 🖼️ Example Slack Conversation

> **@it-bot** How do I connect to the VPN from home?

*Bot replies:*
```
To connect to the VPN from home:
- Ensure you have the latest version of Cisco AnyConnect installed.
- Use your employee credentials (not your personal email).
- If you encounter "Connection Refused," contact IT Service Desk.

*Sources:*
- vpn_troubleshooting_guide.pdf (page 3)
```

---

## 🛠️ Troubleshooting

- **Bot not responding:**  
  - Ensure both backend and Slack bot are running, and tokens are set.
  - Confirm the bot is invited to channel/DM and has correct permissions.
- **PDF issues:**  
  - Check `data/` folder for at least one valid PDF.
  - Run ingestion script after adding or updating PDFs.
- **Backend errors:**  
  - All backend errors are relayed to Slack user.
- **Session issues:**  
  - Session memory is by Slack user ID; each user has a unique, persistent context.

---

## 🧩 Extending

- Add authentication (e.g., restrict to company emails).
- Use Slack Blocks for rich message formatting (buttons, links).
- Integrate human escalation for unresolved queries.
- Analytics for IT trend detection.
- Add support for Word, HTML, or other file types.
- Containerize with Docker/Kubernetes for cloud deployment.

---

## 🔐 Security

- **Never share your bot or API tokens.**
- Use environment variables for all secrets.
- Deploy backend on a secure, internal or VPN-only endpoint for production.

---

## 🎯 Interview/Resume Notes

- **Designed and implemented a RAG-based IT Support Chatbot in Slack, providing instant, context-grounded answers to employee questions by retrieving from official company PDFs using ChromaDB and Cohere.**
- **Integrated with Slack via Bolt SDK for Python, supporting multi-turn conversational memory and secure, stateless operation.**
- **Improved IT support efficiency and reduced ticket volume by enabling self-service in the workplace’s preferred communication platform.**
- **Designed for secure deployment: all keys are managed via environment variables, and session context is handled via mem0 on disk.**
- **Demonstrated robust error handling, session management, and extendability for future cloud, analytics, and compliance integrations.**

---

## 🙏 Credits

- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Cohere](https://cohere.com/)
- [Slack Bolt](https://slack.dev/bolt-python/concepts)
- [mem0](https://github.com/wwt/mem0)
- Built by Rupesh Shivsharan for internal IT support.

---

**Questions or suggestions? Open an issue or PR!**  
**Ready for production and easy to extend.**
