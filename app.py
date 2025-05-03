import streamlit as st
import os
from utils.web_scraper import WebScraper
from utils.summarizer import summarize_text
from utils.pdf_processor import PDFProcessor
import time

# Initialize session state variables
if 'web_scraper' not in st.session_state:
    st.session_state.web_scraper = WebScraper(serpapi_key="a6d98002800a4e1041189bbec17fca2999ff5ff1aef19c981117d76b596bb1c3")
if 'pdf_processor' not in st.session_state:
    st.session_state.pdf_processor = PDFProcessor()
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

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
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border-left: 4px solid #4CAF50;
    }
    .search-result:hover {
        background-color: #e6e9f0;
    }
    .result-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1a73e8;
        margin-bottom: 0.5rem;
    }
    .result-url {
        font-size: 0.9rem;
        color: #5f6368;
        margin-bottom: 0.5rem;
        word-break: break-all;
    }
    .result-snippet {
        font-size: 1rem;
        color: #202124;
        margin-bottom: 1rem;
    }
    .analyze-button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: none;
        cursor: pointer;
    }
    .analyze-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

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
    
    # Search form
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Enter your search query:", key="search_input")
    with col2:
        max_results = st.slider("Max results:", 1, 20, 5, key="max_results")
    
    search_type = st.selectbox("Search type:", ["general", "academic", "news"], key="search_type")
    
    if st.button("Search", key="search_button"):
        if not search_query:
            st.warning("Please enter a search query.")
        else:
            with st.spinner("Searching..."):
                start_time = time.time()
                
                try:
                    # Perform web search
                    st.session_state.search_results = st.session_state.web_scraper.search(
                        query=search_query,
                        max_results=max_results,
                        search_type=search_type
                    )
                    
                    # Display processing time
                    processing_time = time.time() - start_time
                    st.success(f"Search completed in {processing_time:.2f} seconds")
                    
                except Exception as e:
                    st.error(f"An error occurred during search: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
    
    # Display search results
    if st.session_state.search_results:
        st.subheader("Search Results")
        st.markdown(f"Found {len(st.session_state.search_results)} results for '{search_query}'")
        
        for i, result in enumerate(st.session_state.search_results, 1):
            with st.container():
                st.markdown(f"""
                    <div class="search-result">
                        <div class="result-title">{result['title']}</div>
                        <div class="result-url">
                            <a href="{result['url']}" target="_blank">{result['url']}</a>
                        </div>
                        <div class="result-snippet">{result['snippet']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add analyze button
                if st.button(f"Analyze Content {i}", key=f"analyze_{i}"):
                    with st.spinner(f"Analyzing content from {result['title']}..."):
                        try:
                            content = st.session_state.web_scraper.scrape_article(result['url'])
                            if content:
                                st.markdown("### Analysis Results")
                                st.markdown("#### Content")
                                st.write(content[:1000] + "...")
                            else:
                                st.warning("Could not retrieve content from this URL.")
                        except Exception as e:
                            st.error(f"Error analyzing content: {str(e)}")

with tab2:
    st.header("PDF Analysis")
    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Analyze PDF"):
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
                
                # Display content
                st.subheader("Document Content")
                try:
                    if pdf_data['full_text']:
                        st.write(pdf_data['full_text'][:1000] + "...")
                    else:
                        st.warning("No text content found in the PDF.")
                except Exception as e:
                    st.error(f"Error displaying content: {str(e)}")
                
                # Display processing time
                processing_time = time.time() - start_time
                st.metric("Processing Time", f"{processing_time:.2f} seconds")
                
            except Exception as e:
                st.error(f"An error occurred while processing the PDF: {str(e)}")
                import traceback
                st.code(traceback.format_exc()) 