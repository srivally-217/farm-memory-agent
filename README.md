\# Farm Memory Agent



An AI-powered farm assistant that uses persistent memory to remember a farmer's past experiences and provide more personalized responses over time.



\## Problem



Farmers often need to make decisions based on previous crop problems, actions taken, and observed outcomes. A normal chatbot may not reliably remember these experiences across interactions.



Farm Memory Agent addresses this by using Hindsight as a persistent memory layer.



\## How It Works



Farmer

↓

Farm Memory Agent

↓

Hindsight Memory

↓

Relevant Past Farm Experiences

↓

LLM Reasoning

↓

Personalized Response



\## Hindsight Usage



Hindsight is the core memory component of this project.



The application uses Hindsight to:



1\. Retain farm events and experiences as persistent memories.

2\. Recall relevant historical memories when the farmer asks a new question.

3\. Provide those memories to the LLM as context for generating a personalized response.



This allows the agent to use information from previous interactions instead of treating every conversation as completely new.



\## Example



A farmer previously reports:



"Tomato leaves became yellow after heavy rainfall."



The farmer later records:



"The soil was waterlogged, irrigation was reduced, and the leaves later became greener."



When the farmer reports yellow leaves again, the agent can recall these previous experiences and use them when explaining what should be checked.



The system distinguishes between historical observations and current reasoning rather than automatically treating a sequence of events as proven causation.



\## Technology Stack



\- Python

\- FastAPI

\- Hindsight

\- Groq

\- HTML

\- CSS

\- JavaScript



\## Project Structure



FarmMemoryAgent/

├── backend/

│   ├── hindsight\_service.py

│   ├── main.py

│   └── requirements.txt

│

├── frontend/

│   ├── index.html

│   ├── script.js

│   └── style.css

│

└── .gitignore



\## Running Locally



\### 1. Clone the repository



git clone https://github.com/srivally-217/farm-memory-agent.git



cd farm-memory-agent



\### 2. Create a virtual environment



python -m venv venv



\### 3. Activate the virtual environment



Windows:



venv\\Scripts\\activate



\### 4. Install dependencies



pip install -r backend/requirements.txt



\### 5. Configure environment variables



Create a .env file in the project root and add:



HINDSIGHT\_API\_KEY=your\_hindsight\_api\_key

HINDSIGHT\_BASE\_URL=your\_hindsight\_base\_url

GROQ\_API\_KEY=your\_groq\_api\_key



Never commit .env or API keys to GitHub.



\### 6. Start the backend



cd backend



uvicorn main:app --reload



\## Demo Flow



1\. Start with a farmer's farm profile and previous experiences.

2\. Ask about a current crop problem.

3\. The agent recalls relevant historical experiences using Hindsight.

4\. Record a new farm event.

5\. Ask a related question again.

6\. The agent uses the accumulated memory to provide context-aware reasoning.



\## Why Persistent Memory Matters



The key feature of Farm Memory Agent is not simply generating an answer.



The important capability is that the agent can remember what happened on this specific farm and use that history in future interactions.



This enables the system to become more useful as additional farm experiences are recorded.



\## Project Status



Hackathon project demonstrating persistent memory and learning using Hindsight.

