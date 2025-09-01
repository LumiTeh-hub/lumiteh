## Quickly create dependable web automation agents

## What is LumiTeh?

LumiTeh offers everything you need to create and deploy AI agents that interact with the web effortlessly. 
Our end-to-end framework merges AI-driven agents with conventional scripting for peak efficiency—letting you automate predictable tasks with code while leveraging AI only when necessary, reducing costs by over 50% and boosting reliability. 
Build, launch, and scale your own agents and web automations using a single unified API.

## Quickstart

`pip install notte`

`patchright install -with-deps chronium`

# Run in local mode

```python
import lumiteh
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Start a lumiteh session with a visible browser
with lumiteh.Session(headless=False) as session:
    agent = lumiteh.Agent(
        session=session,
        reasoning_model='gemini/gemini-2.5-flash',
        max_steps=30
    )
    
    # Run a task using the agent
    response = agent.run(task="doom scroll cat memes on google images")
```
# Using Python SDK (Recommended)

```python
from lumiteh_sdk import LumiTehClient
import os

# Initialize the LumiTeh client using the API key from environment variables
client = LumiTehClient(api_key=os.getenv("LUMITEH_API_KEY"))

# Start a visible browser session and run tasks with an agent
with client.Session(headless=False) as session:
    agent = client.Agent(
        session=session,
        reasoning_model='gemini/gemini-2.5-flash',
        max_steps=30
    )
    
    # Execute a web automation task using the agent
    response = agent.run(task="doom scroll cat memes on google images")
```
Our configuration lets you test locally and then seamlessly swap the imports and prefix LumiTeh objects with the CLI to switch to the SDK, gaining hosted browser sessions and access to premium features!

## Benchmarks

Rank | Provider | Agent Self-Report | LLM Evaluation | Time per Task | Task Reliability
--- | --- | --- | --- | --- | ---
🏆 | LumiTeh | 86.2% | 79.0% | 47s | 96.6%
2️⃣ | Browser-Use | 77.3% | 60.2% | 113s | 83.3%
3️⃣ | Convergence | 38.4% | 31.4% | 83s | 50%

## Agent features

# Structured output

Structured output lets the agent's `run` function return data in a predefined format by specifying a Pydantic model via the `response_format` parameter. This ensures responses follow the exact structure you define.

```python
from lumiteh_sdk import LumiTehClient
from pydantic import BaseModel
from typing import List

class HackerNewsPost(BaseModel):
    title: str
    url: str
    points: int
    author: str
    comments_count: int

class TopPosts(BaseModel):
    posts: List[HackerNewsPost]

client = LumiTehClient()
with client.Session(headless=False, browser_type="firefox") as session:
    agent = client.Agent(
        session=session,
        reasoning_model='gemini/gemini-2.5-flash',
        max_steps=15
    )
    
    response = agent.run(
        task="Visit Hacker News (news.ycombinator.com) and extract the top 5 posts including titles, URLs, points, authors, and comment counts.",
        response_format=TopPosts
    )

print(response.answer)
```

# Agent Vault

Vaults are secure storage tools you can link to your LumiTeh Agent.
They allow the agent to safely manage credentials and automatically use them when required.

```python
from lumiteh_sdk import LumiTehClient
import os

client = LumiTehClient(api_key=os.getenv("LUMITEH_API_KEY"))

# Using a Vault to securely store credentials and link them to the agent
with client.Vault() as vault, client.Session(headless=False) as session:
    vault.add_credentials(
        url="https://x.com",
        username="your-email",
        password="your-password",
    )
    
    agent = client.Agent(session=session, vault=vault, max_steps=10)
    response = agent.run(
        task="go to twitter; login and go to my messages"
    )

print(response.answer)
```

# Agent Persona

Personas are features you can connect to your LumiTeh Agent to give it unique digital identities, including distinct email addresses, phone numbers, and automatic 2FA management.
from lumiteh_sdk import LumiTehClient

```python
client = LumiTehClient()

with client.Persona(create_phone_number=False) as persona:
    with client.Session(browser_type="firefox", headless=False) as session:
        agent = client.Agent(session=session, persona=persona, max_steps=15)
        response = agent.run(
            task="Open the Google form and RSVP yes with your name",
            url="https://forms.google.com/your-form-url",
        )
print(response.answer)
```

## Session features

# Stealth

Stealth capabilities offer built-in CAPTCHA resolution and proxy management to improve automation reliability and maintain user anonymity.

```python 
from lumiteh_sdk import LumiTehClient
from lumiteh_sdk.types import LumiTehProxy, ExternalProxy

client = LumiTehClient()

# Built-in proxies with automatic CAPTCHA solving
with client.Session(
    solve_captchas=True,
    proxies=True,  # US-based proxy
    browser_type="firefox",
    headless=False
) as session:
    agent = client.Agent(session=session, max_steps=5)
    response = agent.run(
        task="Attempt to solve the CAPTCHA using internal tools",
        url="https://www.google.com/recaptcha/api2/demo"
    )

# Custom proxy configuration
proxy_settings = ExternalProxy(
    server="http://your-proxy-server:port",
    username="your-username",
    password="your-password",
)

with client.Session(proxies=[proxy_settings]) as session:
    agent = client.Agent(session=session, max_steps=5)
    response = agent.run(task="Navigate to a target website")
```

## File download / upload

LumiTeh File Storage enables uploading files to a session and downloading files, that agents acquire while performing tasks. All files are scoped to the session and remain accessible throughout its lifecycle.

```python
from lumiteh_sdk import LumiTehClient

client = LumiTehClient()
storage = client.FileStorage()

# Upload files before running the agent
storage.upload("/path/to/document.pdf")

# Start a session with the storage attached
with client.Session(storage=storage) as session:
    agent = client.Agent(session=session, max_steps=5)
    response = agent.run(
        task="Upload the PDF document to the website and download the cat picture",
        url="https://example.com/upload"
    )

# Download files retrieved by the agent
downloaded_files = storage.list(type="downloads")
for file_name in downloaded_files:
    storage.download(file_name=file_name, local_dir="./results")
```

## Cookies / Auth Sessions

```python
from lumiteh_sdk import LumiTehClient
import json

client = LumiTehClient()

# Upload cookies for authentication
cookies = [
    {
        "name": "sb-db-auth-token",
        "value": "base64-cookie-value",
        "domain": "github.com",
        "path": "/",
        "expires": 9778363203.913704,
        "httpOnly": False,
        "secure": False,
        "sameSite": "Lax"
    }
]

with client.Session() as session:
    session.set_cookies(cookies=cookies)  # or cookie_file="path/to/cookies.json"
    
    agent = client.Agent(session=session, max_steps=5)
    response = agent.run(
        task="go to lumiteh-labs/lumiteh get repo info",
    )
    
    # Retrieve cookies from the session
    cookies_resp = session.get_cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies_resp, f)
```

## License

This project is licensed under the Server Side Public License v1. 
