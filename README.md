# 🔴 AI Agents Travel System using Google ADK 🚀

## Introduction
This project is a multi-agent AI system built using Google’s Agent Development Kit (ADK). It simulates a travel intelligence workflow where multiple agents work together to:

* Retrieve real-time travel information
* Validate structured data
* Audit and correct incorrect travel-related content

The system consists of three main agents:
1. **Travel Scout** – fetches real-time data using Google Search
2. **Geo Validator** – returns structured JSON output
3. **Brochure Auditor** – a multi-agent pipeline (Critic + Reviser)
4. 
# ⚙️ Setup and Creation Steps
## 1️⃣ Install Dependencies
📍 Run in Terminal / Cloud Shell
```bash
export PATH=$PATH:"/home/${USER}/.local/bin"
python3 -m pip install google-adk
pip install -r requirements.txt
```

## 2️⃣ Authenticate Google Cloud
📍 Run in Terminal
```bash
gcloud auth application-default login
```
Follow login in browser → paste code in terminal

## 3️⃣ Create Environment Files
📍 Create `.env` file inside each of these folders:
* `my_google_search_agent/`
* `geo_validator/`
* `llm_auditor/`

### Paste this in ALL `.env` files:
```env
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-2.5-flash
```

# 🔍 Travel Scout Agent Setup
## 📍 Open file:
```text
my_google_search_agent/agent.py
```

## 🔧 Step 1: Add import
👉 At the TOP of the file, add:
```python
from google.adk.tools import google_search
```

## 🔧 Step 2: Modify Agent definition
👉 Find this block (inside the file):
```python
root_agent = Agent(
```
👉 Inside that same block, ADD this line:
```python
tools=[google_search],
```

## ✅ Final result should look like:
```python
root_agent = Agent(
    name="google_search_agent",
    model=os.getenv("MODEL"),
    description="Searches travel info",
    instruction="You are a helpful travel assistant",
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[google_search],
)
```

## ▶️ Run Travel Scout
📍 Run in Terminal:
```bash
cd ~/adk_project
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
```
Open browser:
```
http://127.0.0.1:8000
```
### Test:
```
What are some major events in Tokyo in 2025?
```

# 💻 CLI Verification
📍 Run in Terminal:
```bash
cd ~/adk_project
adk run my_google_search_agent
```

### Test:
```
What is the currency exchange rate for Japan?
```

# 🌍 Geo Validator Setup
## 📍 Open file:
```text
geo_validator/agent.py
```

## 🔧 Step 1: Add import
👉 Add this near top:
```python
from pydantic import BaseModel
```

## 🔧 Step 2: Add schema class
👉 Add this ABOVE the line:
```python
async def main():
```
👉 Add:
```python
class CountryCapital(BaseModel):
    capital: str
```

## 🔧 Step 3: Replace Agent block
👉 Find THIS code:
```python
root_agent = Agent(
    model=model_name,
    name="geo_validator",
    instruction="Answer questions.",
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
)
```

👉 DELETE it and REPLACE with:
```python
root_agent = Agent(
    model=model_name,
    name="geo_validator",
    instruction="Return ONLY the capital city in JSON format.",
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    output_schema=CountryCapital,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
```

## ▶️ Run Geo Validator
📍 Run in Terminal:
```bash
python3 geo_validator/agent.py
```

### Expected Output:

```json
{"capital": "Paris"}
```

# 🧠 Brochure Auditor Setup
## 📍 Open file:

```text
llm_auditor/agent.py
```

## 🔧 Step 1: Enable reviser import
👉 Find this line:
```python
# from .sub_agents.reviser import reviser_agent
```
👉 REMOVE `#` to make it:
```python
from .sub_agents.reviser import reviser_agent
```

## 🔧 Step 2: Replace sub_agents line
👉 Find this line:
```python
sub_agents=[critic_agent]
```
👉 REPLACE it with:
```python
sub_agents=[critic_agent, reviser_agent]
```

## ▶️ Run Brochure Auditor
📍 Run in Terminal:
```bash
cd ~/adk_project
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
```

### Test Input:
```
Double check this: You can take a direct train from Hawaii to Japan.
```

### Expected Result:
* Critic detects error
* Reviser corrects it

# 📌 Conclusion

This project demonstrates how multiple AI agents can collaborate using Google ADK to create intelligent, reliable, and scalable systems. It highlights real-world applications such as travel data retrieval, validation, and automated content correction.
