import streamlit as st
import os
from research_agent import ResearchAgent
from utils.web_scraper import WebScraper
from utils.summarizer import Summarizer
from utils.citation_manager import CitationManager
from utils.pdf_processor import PDFProcessor
from agent_architecture import AgentSystem
from utils.safety_system import SafetySystem
import json
import time

# Initialize the agent system
agent_system = AgentSystem()

# Initialize session state variables
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'pdf_results' not in st.session_state:
    st.session_state.pdf_results = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = None
if 'last_action_params' not in st.session_state:
    st.session_state.last_action_params = None
if 'safety_metrics' not in st.session_state:
    st.session_state.safety_metrics = agent_system.safety_system.get_safety_metrics()
if 'boundaries' not in st.session_state:
    st.session_state.boundaries = agent_system.safety_system.get_boundaries()

# Custom CSS for better styling
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
    .feedback-section {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
    }
    .safety-section {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .error-message {
        color: #dc3545;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Research Assistant Agent")
st.markdown("""
    This research assistant helps you with:
    - Gathering information on research topics
    - Analyzing PDF documents
    - Managing citations
    - Organizing research findings
    - Web search capabilities
    - Learning from your feedback
""")

# Create tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Research Topic", "PDF Analysis", "Web Search", "Agent Feedback"])

with tab1:
    st.header("Research a Topic")
    
    # Input section with agent processing
    topic = st.text_input("Enter your research topic:")
    scope = st.selectbox("Select research scope:", ["general", "detailed"])
    max_results = st.slider("Maximum number of sources:", 1, st.session_state.boundaries['max_research_sources'], 5)
    
    if topic:
        # Process input through agent system
        input_data = {
            'type': 'research_topic',
            'data': {
                'topic': topic,
                'scope': scope,
                'max_results': max_results
            }
        }
        
        try:
            # Get agent response
            agent_response = agent_system.process(input_data)
            
            if st.button("Research"):
                start_time = time.time()
                with st.spinner("Researching..."):
                    # Initialize research agent with parameters from agent system
                    agent = ResearchAgent()
                    results = agent.research_topic(
                        topic,
                        scope=scope,
                        max_results=max_results
                    )
                    
                    # Store results and action info
                    agent_system.memory.store('research_results', results)
                    st.session_state.research_results = results
                    st.session_state.last_action = 'research'
                    st.session_state.last_action_params = {
                        'topic': topic,
                        'scope': scope,
                        'max_results': max_results
                    }
                    
                    # Display results
                    if results:
                        st.success("Research completed!")
                        st.subheader("Research Results")
                        
                        for result in results:
                            with st.expander(f"Source: {result['source']}"):
                                st.markdown(f"**Summary:** {result['summary']}")
                                st.markdown(f"**Key Points:**")
                                for point in result['key_points']:
                                    st.markdown(f"- {point}")
                                st.markdown(f"**Citation:** {result['citation']}")
                                
                                # Add to conversation history
                                agent_system.memory.add_to_history(
                                    'system',
                                    f"Processed research result from {result['source']}"
                                )
                    else:
                        st.warning("No results found. Try adjusting your search terms.")
                        
                    # Show performance metrics
                    st.subheader("Agent Performance")
                    metrics = agent_response['metadata']['performance_metrics']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Research Accuracy", f"{metrics['research_accuracy']:.2%}")
                    with col2:
                        st.metric("Response Time", f"{metrics['response_time']:.2f}s")
                        
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")

with tab2:
    st.header("Analyze PDF Document")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
    
    if uploaded_file:
        # Check file size
        file_size = uploaded_file.size
        if file_size > st.session_state.boundaries['max_file_size_mb'] * 1024 * 1024:
            st.error(f"File size exceeds maximum limit of {st.session_state.boundaries['max_file_size_mb']}MB")
        else:
            # Process input through agent system
            input_data = {
                'type': 'pdf_analysis',
                'data': {
                    'file': uploaded_file,
                    'file_size': file_size
                }
            }
            
            try:
                # Get agent response
                agent_response = agent_system.process(input_data)
                
                if st.button("Analyze PDF"):
                    start_time = time.time()
                    with st.spinner("Analyzing PDF..."):
                        # Save uploaded file
                        file_path = os.path.join("temp", uploaded_file.name)
                        os.makedirs("temp", exist_ok=True)
                        
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Process PDF using agent parameters
                        pdf_processor = PDFProcessor()
                        pdf_data = pdf_processor.process_pdf(file_path)
                        
                        # Store results and action info
                        agent_system.memory.store('pdf_results', pdf_data)
                        st.session_state.pdf_results = pdf_data
                        st.session_state.last_action = 'pdf_analysis'
                        st.session_state.last_action_params = {
                            'file_name': uploaded_file.name,
                            'file_size': file_size
                        }
                        
                        # Display results
                        st.success("PDF Analysis Completed!")
                        
                        # Show document information
                        st.subheader("Document Information")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Title", pdf_data['metadata'].get('title', 'Unknown'))
                        with col2:
                            st.metric("Author", pdf_data['metadata'].get('author', 'Unknown'))
                        with col3:
                            st.metric("Pages", pdf_data['metadata'].get('num_pages', 'Unknown'))
                        
                        # Show sections
                        st.subheader("Document Sections")
                        for section in pdf_data['sections']:
                            with st.expander(f"Section: {section['title']}"):
                                st.write(section['content'])
                        
                        # Generate and show summary
                        st.subheader("Document Summary")
                        summarizer = Summarizer()
                        summary = summarizer.summarize_text(pdf_data['full_text'])
                        st.write(summary)
                        
                        # Show performance metrics
                        st.subheader("Agent Performance")
                        metrics = agent_response['metadata']['performance_metrics']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Analysis Quality", f"{metrics['pdf_analysis_quality']:.2%}")
                        with col2:
                            st.metric("Response Time", f"{metrics['response_time']:.2f}s")
                        
                        # Add to conversation history
                        agent_system.memory.add_to_history(
                            'system',
                            f"Processed PDF document: {uploaded_file.name}"
                        )
                        
                        # Clean up
                        os.remove(file_path)
                        
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")

with tab3:
    st.header("Web Search")
    
    # Search input
    search_query = st.text_input("Enter your search query:")
    
    if search_query:
        # Process input through agent system
        input_data = {
            'type': 'web_search',
            'data': {
                'query': search_query
            }
        }
        
        try:
            # Get agent response
            agent_response = agent_system.process(input_data)
            
            if st.button("Search"):
                start_time = time.time()
                with st.spinner("Searching..."):
                    # Display search results
                    if agent_response['data'].get('search_results'):
                        st.success("Search completed!")
                        st.subheader("Search Results")
                        
                        for result in agent_response['data']['search_results']:
                            with st.container():
                                st.markdown(f"""
                                    <div class="search-result">
                                        <h3>{result['title']}</h3>
                                        <p><strong>URL:</strong> <a href="{result['url']}" target="_blank">{result['url']}</a></p>
                                        <p><strong>Summary:</strong> {result['summary']}</p>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Add to conversation history
                                agent_system.memory.add_to_history(
                                    'system',
                                    f"Processed web search result: {result['title']}"
                                )
                                
                        # Store action info
                        st.session_state.last_action = 'web_search'
                        st.session_state.last_action_params = agent_response['parameters']
                        
                        # Show performance metrics
                        st.subheader("Agent Performance")
                        metrics = agent_response['metadata']['performance_metrics']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Search Relevance", f"{metrics['search_relevance']:.2%}")
                        with col2:
                            st.metric("Response Time", f"{metrics['response_time']:.2f}s")
                    else:
                        st.warning("No results found. Try adjusting your search terms.")
                        
        except Exception as e:
            st.error(f"Error performing search: {str(e)}")
            
    # Show search history
    st.subheader("Recent Searches")
    search_history = agent_system.memory.get_search_history()
    for entry in search_history[-3:]:  # Show last 3 searches
        with st.expander(f"Search: {entry['query']}"):
            st.write(f"Time: {entry['timestamp']}")
            st.write(f"Number of results: {len(entry['results'])}")

with tab4:
    st.header("Agent Feedback")
    
    if st.session_state.last_action:
        st.subheader("Provide Feedback")
        st.write(f"Last action: {st.session_state.last_action}")
        
        # Feedback form
        with st.form("feedback_form"):
            st.write("How would you rate the agent's performance?")
            rating = st.slider("Rating (0-1)", 0.0, 1.0, 0.5, 0.1)
            comments = st.text_area("Additional comments (optional)")
            
            if st.form_submit_button("Submit Feedback"):
                # Process feedback
                feedback_data = {
                    'type': 'feedback',
                    'data': {
                        'action_type': st.session_state.last_action,
                        'action_params': st.session_state.last_action_params,
                        'reward': rating,
                        'comments': comments,
                        'response_time': time.time() - start_time
                    }
                }
                
                try:
                    # Process feedback through agent system
                    agent_response = agent_system.process(feedback_data)
                    st.success("Thank you for your feedback! The agent will learn from it.")
                    
                    # Show updated performance metrics
                    st.subheader("Updated Performance Metrics")
                    metrics = agent_response['metadata']['performance_metrics']
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Research Accuracy", f"{metrics['research_accuracy']:.2%}")
                    with col2:
                        st.metric("PDF Analysis Quality", f"{metrics['pdf_analysis_quality']:.2%}")
                    with col3:
                        st.metric("Search Relevance", f"{metrics['search_relevance']:.2%}")
                        
                except Exception as e:
                    st.error(f"Error processing feedback: {str(e)}")
    else:
        st.info("Complete an action (research, PDF analysis, or web search) to provide feedback.")

# Add a section to view agent memory and processing
with st.sidebar:
    st.header("Agent System Info")
    
    # Show memory contents
    if st.button("View Agent Memory"):
        memory_contents = agent_system.memory.memory_store
        st.json(memory_contents)
    
    # Show processing history
    st.subheader("Processing History")
    history = agent_system.memory.get_history()
    for entry in history[-5:]:  # Show last 5 entries
        st.text(f"{entry['role']}: {entry['content'][:100]}...")
        
    # Show learning rates
    st.subheader("Learning Rates")
    learning_rates = agent_system.feedback_system.get_learning_rates()
    for action_type, rate in learning_rates.items():
        st.metric(f"{action_type.title()} Learning Rate", f"{rate:.3f}")

# Display safety information
st.sidebar.markdown("---")
st.sidebar.header("Safety Information")
st.sidebar.subheader("Operational Boundaries")
for boundary, value in st.session_state.boundaries.items():
    st.sidebar.metric(boundary.replace('_', ' ').title(), str(value))

st.sidebar.subheader("Restricted Content")
restricted_patterns = agent_system.safety_system.get_restricted_patterns()
for category, patterns in restricted_patterns.items():
    with st.sidebar.expander(category.replace('_', ' ').title()):
        for pattern in patterns:
            st.text(pattern) 