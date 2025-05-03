# Research Assistant

A Streamlit-based research assistant application that helps with web search and PDF analysis.

## Features

- Web search capabilities with customizable search types
- PDF document analysis and summarization
- Content analysis using OpenAI's API
- Modern and user-friendly interface

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter your OpenAI API key in the sidebar if not already set in the `.env` file

4. Use the application:
   - Web Search tab: Enter a search query and customize search parameters
   - PDF Analysis tab: Upload and analyze PDF documents

## Project Structure

- `app.py`: Main Streamlit application
- `utils/`: Utility modules
  - `web_scraper.py`: Web search and content scraping
  - `summarizer.py`: Text summarization using OpenAI
  - `pdf_processor.py`: PDF document processing
  - `__init__.py`: Package initialization

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for web search functionality 