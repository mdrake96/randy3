# Research Assistant Agent

An intelligent agent that helps users research topics, gather information, and present findings in an organized format.

## Features

- Information retrieval and summarization from multiple sources
- Evaluation of source credibility and relevance
- Organization of findings into structured reports
- Citation management and reference tracking
- Web interface using Streamlit

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your API keys:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Command Line Usage

```python
from research_agent import ResearchAgent

# Initialize the agent
agent = ResearchAgent()

# Start a research session
results = agent.research_topic(
    topic="Your research topic",
    max_sources=5,
    include_citations=True
)

# Get a structured report
report = agent.generate_report(results)
```

### Web Interface (Streamlit)

To run the web interface:

```bash
streamlit run app.py
```

The web interface provides:
- Topic input field
- Settings for number of sources and citation style
- Real-time research progress
- Interactive display of results
- Downloadable research reports

## Project Structure

- `research_agent.py`: Main agent implementation
- `app.py`: Streamlit web interface
- `utils/`: Helper functions and utilities
  - `web_scraper.py`: Web scraping functionality
  - `summarizer.py`: Text summarization utilities
  - `citation_manager.py`: Citation formatting and management

## Deployment

### Local Deployment

1. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

### Cloud Deployment

You can deploy the app to Streamlit Cloud:

1. Create a GitHub repository with your code
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Set the following environment variables in the Streamlit Cloud settings:
   - `OPENAI_API_KEY`: Your OpenAI API key

## License

MIT License 