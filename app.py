import streamlit as st
import os
from utils.web_scraper import WebScraper
from utils.summarizer import summarize_text
from utils.pdf_processor import PDFProcessor
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize session state variables
if 'api_key' not in st.session_state:
    st.session_state.api_key = openai_api_key
if 'web_scraper' not in st.session_state:
    st.session_state.web_scraper = WebScraper()
if 'pdf_processor' not in st.session_state:
    st.session_state.pdf_processor = PDFProcessor()

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        font-size: 1.1rem;
    }
    .stMarkdown {
        font-size: 1.1rem;
    }
    .search-result {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# API Key input in sidebar
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input("Enter your OpenAI API key:", type="password", value=st.session_state.api_key if st.session_state.api_key else "")
if api_key_input:
    st.session_state.api_key = api_key_input

# Main content
if not st.session_state.api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()

st.title("Research Assistant")
st.markdown("""
    This research assistant helps you with:
    - Web search capabilities
    - PDF document analysis
    - Content summarization
    - Information analysis
""")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Web Search", "PDF Analysis"])

with tab1:
    st.header("Web Search")
    search_query = st.text_input("Enter your search query:")
    max_results = st.slider("Maximum number of results:", 1, 20, 5)
    search_type = st.selectbox("Search type:", ["general", "academic", "news"])
    
    if st.button("Search"):
        if not st.session_state.api_key:
            st.error("Please enter your OpenAI API key in the sidebar first.")
        else:
            start_time = time.time()
            
            try:
                # Perform web search
                search_results = st.session_state.web_scraper.search(
                    query=search_query,
                    max_results=max_results,
                    search_type=search_type
                )
                
                # Display search results
                st.subheader("Search Results")
                for i, result in enumerate(search_results, 1):
                    with st.expander(f"Result {i}: {result['title']}"):
                        st.write(f"**URL:** {result['url']}")
                        st.write(f"**Snippet:** {result['snippet']}")
                        
                        # Add option to analyze the content
                        if st.button(f"Analyze Content {i}"):
                            content = st.session_state.web_scraper.scrape_article(result['url'])
                            if content:
                                # Generate summary
                                summary = summarize_text(content, api_key=st.session_state.api_key)
                                st.write("**Summary:**")
                                st.write(summary)
                
                # Display processing time
                processing_time = time.time() - start_time
                st.metric("Processing Time", f"{processing_time:.2f} seconds")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

with tab2:
    st.header("PDF Analysis")
    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Analyze PDF"):
            if not st.session_state.api_key:
                st.error("Please enter your OpenAI API key in the sidebar first.")
            else:
                start_time = time.time()
                
                try:
                    # Process PDF
                    st.write("Processing PDF...")
                    pdf_data = st.session_state.pdf_processor.process_pdf(uploaded_file)
                    
                    if not pdf_data:
                        st.error("Failed to process PDF. The processor returned None.")
                        st.stop()
                    
                    # Display document information
                    st.subheader("Document Information")
                    try:
                        st.write(f"Title: {pdf_data['metadata']['title']}")
                        st.write(f"Author: {pdf_data['metadata']['author']}")
                        st.write(f"Page Count: {pdf_data['metadata']['page_count']}")
                    except Exception as e:
                        st.error(f"Error displaying document information: {str(e)}")
                        st.write("PDF Data structure:", pdf_data)
                    
                    # Display sections
                    st.subheader("Document Sections")
                    try:
                        for section in pdf_data['sections']:
                            with st.expander(section['title']):
                                st.write(section['content'])
                    except Exception as e:
                        st.error(f"Error displaying sections: {str(e)}")
                    
                    # Display summary
                    st.subheader("Document Summary")
                    try:
                        if pdf_data['full_text']:
                            summary = summarize_text(pdf_data['full_text'], api_key=st.session_state.api_key)
                            st.write(summary)
                        else:
                            st.warning("No text content found in the PDF.")
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
                    
                    # Display processing time
                    processing_time = time.time() - start_time
                    st.metric("Processing Time", f"{processing_time:.2f} seconds")
                    
                except Exception as e:
                    st.error(f"An error occurred while processing the PDF: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc()) 