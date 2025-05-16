
# 🤖 Automated Customer Query Resolution for Insurance using Agent AI

This project enables **real-time, AI-powered customer support** for insurance companies using a chat interface. Built with **Streamlit**, **n8n**, **Supabase**, **Groq LLaMA 70B**, and **Mistral Embeddings**, it acts as an open-source alternative to AWS Connect—optimized for scalability, cost-efficiency, and document-grounded AI reasoning.

---

## 📁 Repository Structure

```
📦 insurance-ai-chatbot/
 ┣ 📄 README.md
 ┣ 📄 n8n-streamlit.py           # Frontend UI using Streamlit
 ┣ 📄 Main_2.json                # n8n main workflow for chat handling
 ┣ 📄 requirements.txt           # Python dependencies
```

---

## 🚀 Features

- 🔐 Supabase authentication for secure access
- 💬 Chat UI for policyholders with session continuity
- 📂 Google Drive-based insurance data ingestion
- 🧠 Retrieval-Augmented Generation using Groq + Mistral
- 🗃️ Supabase Vector Store integration
- 👨‍💼 Agent dashboard to review chat history by session
- 📉 Cost-effective alternative to AWS Connect

---

## 🛠️ Technologies Used

| Layer            | Tool/Service                 |
|------------------|------------------------------|
| Frontend         | Streamlit                    |
| Workflow Engine  | n8n                          |
| Database & Auth  | Supabase (PostgreSQL + Auth) |
| Embeddings       | Mistral AI                   |
| LLM Inference    | Groq API (LLaMA 70B)         |
| File Trigger     | Google Drive API             |

---

## 🔄 Workflow Overview

### 1. Data Ingestion
- Upload `.csv` file with insurance data to Google Drive
- Trigger n8n ingestion workflow:
  - Split data with Recursive Text Splitter
  - Convert to embeddings with Mistral
  - Store in Supabase vector DB

### 2. User Interaction
- User logs in via Streamlit frontend
- Sends query → triggers `invoke-supabase-agent` webhook
- n8n retrieves session + vectors → Groq generates response
- Chat logged to Supabase and returned to user

---

## ▶️ Running the Project

### 🔧 1. Clone the Repository
```bash
git clone https://github.com/yourusername/insurance-ai-chatbot.git
cd insurance-ai-chatbot
```

### 📦 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 💬 3. Run the Streamlit App
```bash
streamlit run n8n-streamlit.py
```

---

## 📂 Files

### `n8n-streamlit.py`
- Secure login with Supabase Auth
- Chat interface with session tracking
- Sends/receives messages via n8n webhook

### `Main_2.json`
- The main **n8n workflow** for:
  - Authenticating users
  - Querying vector DB
  - Fetching chat history
  - Invoking LLM via Groq
  - Returning structured response

---



## 📈 Future Enhancements

- 🎙️ Voice assistant integration using Whisper + Groq
- 📊 Analytics dashboard for unresolved queries and user trends
- 🧑‍💼 Admin portal for file uploads and agent escalation tracking
- 🔁 Multi-channel integration (email, WhatsApp, IVR)
- 🔗 MCP client-server support

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [Supabase](https://supabase.com/)
- [Groq](https://groq.com/)
- [Mistral AI](https://mistral.ai/)
- [n8n](https://n8n.io/)
- [Streamlit](https://streamlit.io/)

---

## 👨‍💻 Author

**Sivasurya P**  
_Final Year CSE Student, Thiagarajar College of Engineering_
