# paper-qa-agent
## Setup
### .env file setup
Create a `.env` file from this template. Fill in your own OpenAI API Key.
```
WCS_URL=https://tobys-sandbox-oo0vfo50.weaviate.network
WCS_API_KEY=HaDolSevqI9HxhvwMnl9DssgKMObfc0eXfC7
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
### Install dependencies
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Usage
Use 'query_qa_rag_agent.ipynb'

## Architecture
![Architecture Diagram](architecture.png)

## Tech Debt
- `retrievers.py` and `vector_dbs.py` have some duplicate code