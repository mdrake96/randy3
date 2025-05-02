import streamlit as st
from research_agent import ResearchAgent
from utils.pdf_processor import PDFProcessor
import os
from dotenv import load_dotenv
import time

# Set page config
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Initialize session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'pdf_results' not in st.session_state:
    st.session_state.pdf_results = None

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .report-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .tab-content {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 Research Assistant")
st.markdown("""
    This tool helps you research topics, gather information, and present findings in an organized format.
    You can either research a topic or analyze a PDF document.
""")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Research Topic", "PDF Analysis"])

with tab1:
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        max_sources = st.slider("Maximum number of sources", 1, 10, 5)
        include_citations = st.checkbox("Include citations", value=True)
        citation_style = st.selectbox(
            "Citation style",
            ["APA", "MLA", "Chicago"],
            index=0
        )

    # Main content for research
    topic = st.text_input("Enter your research topic", placeholder="e.g., Climate change effects on marine ecosystems")

    if st.button("Research", type="primary"):
        if not topic:
            st.error("Please enter a research topic")
        else:
            try:
                with st.spinner("Researching... This may take a few minutes."):
                    # Initialize agent
                    agent = ResearchAgent()
                    
                    # Start research
                    st.session_state.research_results = agent.research_topic(
                        topic=topic,
                        max_sources=max_sources,
                        include_citations=include_citations
                    )
                    
                    # Generate report
                    report = agent.generate_report(st.session_state.research_results)
                    
                    # Display results
                    st.success("Research completed!")
                    
                    # Show overall summary
                    st.subheader("Overall Summary")
                    st.markdown(f"<div class='report-box'>{report.split('## Sources')[0]}</div>", unsafe_allow_html=True)
                    
                    # Show sources
                    st.subheader("Sources")
                    for source in st.session_state.research_results['sources']:
                        with st.expander(f"{source['title']} (Credibility: {source['credibility_score']}/10)"):
                            st.markdown(f"**URL:** {source['url']}")
                            st.markdown(f"**Summary:** {source['summary']}")
                    
                    # Show citations if enabled
                    if include_citations and st.session_state.research_results['citations']:
                        st.subheader("References")
                        for citation in st.session_state.research_results['citations']:
                            st.markdown(f"- {citation}")
                    
                    # Download button for report
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"research_report_{topic.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

with tab2:
    # PDF Analysis section
    st.header("PDF Document Analysis")
    
    uploaded_file = st.file_uploader("Upload a PDF document", type=['pdf'])
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing PDF..."):
                # Initialize PDF processor
                pdf_processor = PDFProcessor()
                
                # Process PDF
                pdf_data = pdf_processor.process_pdf(uploaded_file.read())
                
                if pdf_data:
                    st.session_state.pdf_results = pdf_data
                    
                    # Display PDF information
                    st.success("PDF processed successfully!")
                    
                    # Show document info
                    st.subheader("Document Information")
                    st.markdown(f"**Title:** {pdf_data['title']}")
                    st.markdown(f"**Author:** {pdf_data['author']}")
                    st.markdown(f"**Number of Pages:** {pdf_data['num_pages']}")
                    
                    # Extract and display sections
                    sections = pdf_processor.extract_sections(pdf_data['text'])
                    
                    st.subheader("Document Sections")
                    for section in sections:
                        with st.expander(section['title']):
                            st.markdown(section['content'])
                    
                    # Generate summary using research agent
                    st.subheader("Document Summary")
                    agent = ResearchAgent()
                    summary = agent._summarize_content(pdf_data['text'])
                    st.markdown(f"<div class='report-box'>{summary}</div>", unsafe_allow_html=True)
                    
                    # Download extracted text
                    st.download_button(
                        label="Download Extracted Text",
                        data=pdf_data['text'],
                        file_name=f"{pdf_data['title'].replace(' ', '_')}_extracted.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Failed to process PDF file")
                    
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Research Assistant v1.0 | Powered by OpenAI</p>
    </div>
""", unsafe_allow_html=True) 