# Gmail Agentic AI

A locally-runnable Gmail assistant powered by **IBM WatsonX** (`ibm/granite-4-h-small`) and **LangChain**.  
Send plain-English commands to list, read, write, or permanently delete emails from your Gmail inbox via a single `POST /chat` API endpoint.

---

## Local URLs (after startup)

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000` | Health check |
| **`http://127.0.0.1:8000/docs`** | **Swagger UI — interactive testing (start here)** |
| `POST http://127.0.0.1:8000/chat` | Natural language chat endpoint |

---

## Prerequisites

- Python **3.9+**
- A **Google Cloud** account (free tier is fine)
- An **IBM WatsonX** account with an active project

---

## Step 1 — Google Cloud Setup

### 1a. Enable the Gmail API
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Select or create a project
3. Navigate to **APIs & Services → Library**
4. Search for **Gmail API** and click **Enable**

### 1b. Configure the OAuth Consent Screen
1. Go to **APIs & Services → OAuth consent screen**
2. Choose **External** (or Internal if using Google Workspace)
3. Fill in App name, User support email, Developer contact email → **Save and Continue**
4. On the **Scopes** step click **Add or Remove Scopes**
5. Add the scope: `https://mail.google.com/`  → **Save and Continue**
6. On the **Test users** step, add your Gmail address → **Save and Continue**

### 1c. Create OAuth2 Credentials
1. Go to **APIs & Services → Credentials**
2. Click **+ Create Credentials → OAuth client ID**
3. Application type: **Desktop app**
4. Give it a name (e.g. `Gmail Agent`) → **Create**
5. Click **Download JSON** — save the file as **`credentials.json`** in the `gmail-agent/` folder

---

## Step 2 — IBM WatsonX Setup

| What you need | Where to find it |
|---|---|
| **API Key** | [IBM Cloud](https://cloud.ibm.com) → Manage → API Keys → Create |
| **Project ID** | [WatsonX.ai](https://dataplatform.cloud.ibm.com) → Your project → Manage tab → General → Project ID |
| **URL** | `https://us-south.ml.cloud.ibm.com` (us-south region) |

---

## Step 3 — Installation

```bash
# Clone / navigate to the project folder
cd gmail-agent

# (Recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4 — Configuration

```bash
# Copy the template
copy .env.example .env      # Windows
# cp .env.example .env      # macOS / Linux
```

Open `.env` and fill in your values:

```env
WATSONX_API_KEY=your_actual_api_key
WATSONX_PROJECT_ID=your_actual_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Make sure `credentials.json` (downloaded in Step 1c) is in the `gmail-agent/` folder.

---

## Step 5 — Run

```bash
uvicorn main:app --reload
```

**First run only:** A browser window will open automatically for the Google OAuth2 consent screen.  
Log in with your Gmail account, grant access → the browser redirects and closes.  
A `token.json` file is saved locally — you won't be prompted again.

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## Step 6 — Usage

### Option A — Swagger UI (easiest)
Open **`http://127.0.0.1:8000/docs`** in your browser.  
Click `POST /chat` → **Try it out** → enter your message → **Execute**.

### Option B — curl

**List emails:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"List my last 5 emails\"}"
```

**Read an email:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Read the email with ID 18f3a2b1c4d5e6f7\"}"
```

**Send an email:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Send an email to alice@example.com with subject Meeting Tomorrow and body Hi Alice, are you free at 10am?\"}"
```

**Delete an email:**
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Permanently delete the email with ID 18f3a2b1c4d5e6f7\"}"
```

### Option C — Python requests

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"message": "List my last 5 unread emails"}
)
print(response.json()["reply"])
```

---

## Project Structure

```
gmail-agent/
├── main.py            ← FastAPI app — POST /chat endpoint
├── agent.py           ← LangChain ReAct agent + WatsonX LLM
├── gmail_tools.py     ← 4 LangChain tools: list, read, send, delete
├── gmail_auth.py      ← OAuth2 browser flow → token.json
├── credentials.json   ← Downloaded from Google Cloud Console (not committed)
├── token.json         ← Auto-generated on first run (not committed)
├── .env               ← Your secrets (not committed)
├── .env.example       ← Template — copy to .env and fill in values
├── requirements.txt   ← Python dependencies
└── README.md
```

---

## Available Agent Commands (Examples)

| Intent | Example message |
|---|---|
| List emails | `"List my last 5 emails"` |
| List unread | `"Show me my unread emails"` |
| List from sender | `"Show emails from boss@company.com"` |
| Read email | `"Read email ID 18f3a2b1c4d5e6f7"` |
| Send email | `"Send an email to alice@example.com with subject Hi and body Hello!"` |
| Delete email | `"Permanently delete email ID 18f3a2b1c4d5e6f7"` |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `credentials.json not found` | Download OAuth client JSON from Google Cloud Console and place it in `gmail-agent/` |
| `WATSONX_API_KEY not set` | Ensure `.env` exists with all three WatsonX variables filled in |
| Browser doesn't open for OAuth | Run from a machine with a browser; or set `DISPLAY` on Linux |
| `Token has been expired or revoked` | Delete `token.json` and run again to re-authenticate |
| Agent loops without answering | Check that `ibm/granite-4-h-small` is available in your WatsonX project region |
