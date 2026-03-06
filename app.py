"""
Main Streamlit Application - AI Interview Coach
Professional Edition v1.0
"""
# Add these imports at the top with other imports
from utils import (
    get_typing_animation, get_confetti_animation, get_robot_avatar,
    get_loading_spinner, get_progress_ring, get_welcome_animation,
    get_success_animation
)

# Import your custom modules
from knowledge_base import KnowledgeBase
from question_selector import QuestionSelector
from answer_evaluator import AnswerEvaluator
from performance_report import PerformanceReport
from utils import *
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import json

# Import your custom modules
from knowledge_base import KnowledgeBase
from question_selector import QuestionSelector
from answer_evaluator import AnswerEvaluator
from performance_report import PerformanceReport
from utils import *

# Page configuration
st.set_page_config(
    page_title="AI Interview Coach - Professional Edition",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# PROFESSIONAL CSS STYLING
# =============================================================================
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Professional headers */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        animation: fadeIn 1s ease-in;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #718096;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
        animation: slideUp 0.8s ease-out;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Card styling */
    .css-1r6slb0, .stCard {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .css-1r6slb0:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Form styling */
    .stForm {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Select boxes */
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.5rem;
        font-size: 1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 10px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%);
        color: #22543d;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #48bb78;
        animation: slideIn 0.5s ease;
    }
    
    .stError {
        background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
        color: #742a2a;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f56565;
        animation: slideIn 0.5s ease;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #feebc8 0%, #fbd38d 100%);
        color: #7b341e;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ed8936;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f7fafc;
        padding: 0.5rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: none;
        border-radius: 10px;
        color: #718096;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        border-radius: 10px;
        font-weight: 500;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e4e8f0 0%, #d0d9e8 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #a0aec0;
        font-size: 0.9rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }
    
    /* Professional badges */
    .badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0.25rem;
    }
    
    .badge-beginner {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 1px solid #fbbf24;
    }
    
    .badge-intermediate {
        background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%);
        color: #1e40af;
        border: 1px solid #3b82f6;
    }
    
    .badge-advanced {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
        color: #991b1b;
        border: 1px solid #ef4444;
    }
    
    .badge-expert {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 1px solid #10b981;
    }
    
    /* Question box */
    .question-box {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #667eea;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }
    
    .question-text {
        font-size: 1.3rem;
        font-weight: 500;
        color: #1e293b;
        line-height: 1.6;
    }
    
    .question-meta {
        color: #475569;
        font-size: 0.9rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Feedback box */
    .feedback-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    /* Score colors */
    .score-high {
        color: #10b981;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .score-medium {
        color: #f59e0b;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .score-low {
        color: #ef4444;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Headers in sidebar */
    .sidebar-header {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1rem;
        }
        
        .question-text {
            font-size: 1.1rem;
        }
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea transparent #667eea transparent !important;
    }
    
    /* Checkbox */
    .stCheckbox > div > label > div:first-child {
        background-color: #667eea !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        gap: 1rem;
    }
    
    .stRadio > div > label {
        background: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stRadio > div > label:hover {
        border-color: #667eea;
        background: #f0f4ff;
    }
    
    /* Tooltip */
    .stTooltip {
        background: #1e293b;
        color: white;
        border-radius: 5px;
        padding: 0.5rem;
        font-size: 0.85rem;
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: 0;
        height: 1px;
        background: linear-gradient(135deg, transparent, #667eea, transparent);
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# INITIALIZE SESSION STATE
# =============================================================================
def init_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.kb = KnowledgeBase()
        st.session_state.selector = QuestionSelector(st.session_state.kb)
        st.session_state.evaluator = AnswerEvaluator(st.session_state.kb)
        st.session_state.reporter = PerformanceReport()
        st.session_state.messages = []
        st.session_state.current_question = None
        st.session_state.question_history = []
        st.session_state.answer_history = []
        st.session_state.interview_active = False
        st.session_state.interview_complete = False
        st.session_state.user_profile = {}
        st.session_state.report = None
        st.session_state.current_feedback = None
        st.session_state.session_start_time = datetime.now()
        st.session_state.total_sessions = 0
        st.session_state.questions_answered = 0

# Call initialization
init_session_state()

# =============================================================================
# SIDEBAR - PROFESSIONAL PROFILE FORM
# =============================================================================
with st.sidebar:
    # Professional Header with Logo
    st.markdown("""
        <div style="text-align: center; padding: 20px 10px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 15px;
                        display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);">
                <span style="font-size: 3rem; color: white;">🎯</span>
            </div>
            <h2 style="color: #1E293B; margin: 0; font-size: 1.8rem;">AI Interview Coach</h2>
            <p style="color: #64748B; margin: 5px 0 0; font-size: 0.9rem;">Professional Edition v2.0</p>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        height: 3px; width: 50px; margin: 15px auto 0; border-radius: 3px;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User Profile Section with Professional Styling
    st.markdown("""
        <div class="sidebar-header">
            👤 Candidate Profile
        </div>
        <p style='color: #64748B; font-size: 0.85rem; margin: 5px 0 15px;'>
            Complete your profile to begin the assessment
        </p>
    """, unsafe_allow_html=True)
    
    # Professional Form
    with st.form("professional_profile_form", clear_on_submit=False):
        # Personal Information Section
        st.markdown("##### 📋 Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "Full Name*",
                value=st.session_state.user_profile.get("name", ""),
                placeholder="John Doe",
                help="Enter your full legal name"
            )
        
        with col2:
            email = st.text_input(
                "Email Address*",
                value=st.session_state.user_profile.get("email", ""),
                placeholder="john.doe@example.com",
                help="We'll send your assessment reports here"
            )
        
        st.markdown("---")
        
        # Professional Details
        st.markdown("##### 🎯 Career Goals")
        
        target_role = st.selectbox(
            "Target Position*",
            options=[
                "Software Engineer",
                "Data Scientist",
                "Backend Developer",
                "Frontend Developer",
                "DevOps Engineer",
                "Data Analyst",
                "Machine Learning Engineer",
                "Full Stack Developer",
                "Cloud Architect",
                "Product Manager",
                "QA Engineer",
                "Systems Administrator"
            ],
            index=0,
            help="Select the role you're preparing for"
        )
        
        # Experience Level with Professional Grading
        st.markdown("##### 📊 Experience Level")
        
        experience = st.radio(
            "Select your experience level*",
            options=[
                "Entry Level (0-2 years)",
                "Mid Level (3-5 years)",
                "Senior Level (5+ years)",
                "Lead/Manager (8+ years)"
            ],
            index=0,
            horizontal=False,
            help="Your current professional experience level"
        )
        
        # Skills Selection with Categories
        st.markdown("##### 💻 Technical Skills")
        
        col1, col2 = st.columns(2)
        with col1:
            programming_languages = st.multiselect(
                "Programming Languages",
                options=["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust", "PHP", "Swift", "Kotlin"],
                default=[s for s in st.session_state.user_profile.get("skills", []) if s in ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust", "PHP", "Swift", "Kotlin"]]
            )
            
            databases = st.multiselect(
                "Databases",
                options=["SQL", "MongoDB", "PostgreSQL", "MySQL", "Oracle", "Redis", "Elasticsearch"],
                default=[s for s in st.session_state.user_profile.get("skills", []) if s in ["SQL", "MongoDB", "PostgreSQL", "MySQL", "Oracle", "Redis", "Elasticsearch"]]
            )
        
        with col2:
            frameworks = st.multiselect(
                "Frameworks & Libraries",
                options=["React", "Node.js", "Django", "Flask", "Spring", "Angular", "Vue.js", "TensorFlow", "PyTorch"],
                default=[s for s in st.session_state.user_profile.get("skills", []) if s in ["React", "Node.js", "Django", "Flask", "Spring", "Angular", "Vue.js", "TensorFlow", "PyTorch"]]
            )
            
            tools = st.multiselect(
                "Tools & Platforms",
                options=["AWS", "Docker", "Kubernetes", "Git", "Linux", "Jenkins", "Terraform", "Ansible"],
                default=[s for s in st.session_state.user_profile.get("skills", []) if s in ["AWS", "Docker", "Kubernetes", "Git", "Linux", "Jenkins", "Terraform", "Ansible"]]
            )
        
        # Combine all skills
        all_skills = programming_languages + databases + frameworks + tools
        
        # Additional Information (Optional)
        with st.expander("📋 Additional Information (Optional)"):
            col1, col2 = st.columns(2)
            with col1:
                linkedin = st.text_input(
                    "LinkedIn Profile",
                    placeholder="https://linkedin.com/in/username"
                )
                github = st.text_input(
                    "GitHub Profile",
                    placeholder="https://github.com/username"
                )
            
            with col2:
                years_exp = st.slider(
                    "Years of Experience",
                    min_value=0,
                    max_value=30,
                    value=st.session_state.user_profile.get("years_experience", 2),
                    step=1
                )
                
                education = st.selectbox(
                    "Highest Education",
                    options=["High School", "Bachelor's", "Master's", "PhD", "Bootcamp", "Self-taught"],
                    index=1
                )
        
        st.markdown("---")
        
        # Submit Button with Professional Styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 SAVE PROFILE & START",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            # Validation
            errors = []
            if not name:
                errors.append("Name is required")
            if not email:
                errors.append("Email is required")
            elif "@" not in email or "." not in email:
                errors.append("Please enter a valid email address")
            if len(all_skills) < 2:
                errors.append("Please select at least 2 skills")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Save to session state
                st.session_state.user_profile = {
                    "name": name,
                    "email": email,
                    "target_role": target_role,
                    "experience_level": experience.split("(")[0].strip().lower(),
                    "skills": all_skills,
                    "linkedin": linkedin,
                    "github": github,
                    "years_experience": years_exp,
                    "education": education,
                    "profile_complete": True,
                    "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Success message with animation
                st.success("""
                    ✅ Profile Saved Successfully!
                    
                    You're all set to begin your interview practice.
                    Click 'Start Interview' below to begin.
                """)
                st.balloons()
                
                # Show profile summary
                with st.expander("📊 Profile Summary"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Name:**", name)
                        st.write("**Role:**", target_role)
                        st.write("**Level:**", experience)
                    with col2:
                        st.write("**Skills:**", len(all_skills))
                        st.write("**Experience:**", years_exp, "years")
    
    st.markdown("---")
    
    # Interview Controls
    st.markdown("""
        <div class="sidebar-header">
            🎮 Interview Controls
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.interview_active and not st.session_state.interview_complete:
        if st.button("🚀 START NEW INTERVIEW", use_container_width=True):
            if st.session_state.user_profile:
                st.session_state.interview_active = True
                st.session_state.messages = []
                st.session_state.question_history = []
                st.session_state.answer_history = []
                st.session_state.current_question = st.session_state.selector.select_next_question(
                    st.session_state.user_profile, []
                )
                st.rerun()
            else:
                st.warning("⚠️ Please save your profile first!")
    
    if st.session_state.interview_active:
        if st.button("⏹️ END INTERVIEW", use_container_width=True):
            st.session_state.interview_active = False
            st.session_state.interview_complete = True
            # Generate final report
            with st.spinner("Generating your performance report..."):
                st.session_state.report = st.session_state.reporter.generate_report(
                    st.session_state.user_profile,
                    st.session_state.answer_history
                )
            st.success("✅ Interview completed! Check your report below.")
            st.rerun()
    
    if st.session_state.interview_complete:
        if st.button("🔄 START NEW SESSION", use_container_width=True):
            st.session_state.interview_active = False
            st.session_state.interview_complete = False
            st.session_state.current_question = None
            st.session_state.messages = []
            st.session_state.question_history = []
            st.session_state.answer_history = []
            st.session_state.report = None
            st.rerun()
    
    st.markdown("---")
    
    # Session Statistics
    if st.session_state.user_profile:
        st.markdown("""
            <div class="sidebar-header">
                📊 Session Statistics
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div style="font-size: 1.5rem; color: #667eea;">📝</div>
                    <div class="metric-value">""" + str(len(st.session_state.answer_history)) + """</div>
                    <div class="metric-label">Questions</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.answer_history:
                avg_score = sum([a.get("score", 0) for a in st.session_state.answer_history]) / len(st.session_state.answer_history)
                score_color = "score-high" if avg_score >= 7 else "score-medium" if avg_score >= 5 else "score-low"
                st.markdown("""
                    <div class="metric-card">
                        <div style="font-size: 1.5rem; color: #667eea;">⭐</div>
                        <div class="metric-value"><span class='""" + score_color + """'>""" + f"{avg_score:.1f}" + """/10</span></div>
                        <div class="metric-label">Average Score</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="metric-card">
                        <div style="font-size: 1.5rem; color: #667eea;">⭐</div>
                        <div class="metric-value">0/10</div>
                        <div class="metric-label">Average Score</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Progress bar
        if st.session_state.answer_history:
            progress = min(len(st.session_state.answer_history) / 10, 1.0)
            st.progress(progress)
            st.write(f"**Progress:** {len(st.session_state.answer_history)}/10 questions")
    
    st.markdown("---")
    
    # Quick Tips
    with st.expander("💡 Quick Tips"):
        st.markdown("""
            - Be specific in your answers
            - Include examples from experience
            - Explain concepts in your own words
            - Practice regularly for best results
            - Review feedback after each answer
        """)

# =============================================================================
# MAIN CONTENT AREA
# =============================================================================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="main-header">🎯 AI Interview Coach</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional Interview Preparation with Real-time AI Feedback</p>', unsafe_allow_html=True)

# =============================================================================
# WELCOME SECTION (No Active Interview)
# =============================================================================
if not st.session_state.interview_active and not st.session_state.interview_complete:
    # Welcome Banner
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 3rem;
                    border-radius: 20px;
                    margin: 2rem 0;
                    color: white;
                    text-align: center;
                    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);">
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">Welcome to Your AI Interview Coach!</h2>
            <p style="font-size: 1.2rem; opacity: 0.9;">Master your interview skills with personalized AI feedback</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h3>Personalized Questions</h3>
                <p style="color: #666;">Questions tailored to your target role and experience level using intelligent algorithms</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3>AI-Powered Feedback</h3>
                <p style="color: #666;">Instant evaluation with strengths, weaknesses, and ideal answer examples</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3>Detailed Analytics</h3>
                <p style="color: #666;">Comprehensive performance reports with learning path recommendations</p>
            </div>
        """, unsafe_allow_html=True)
    
    # How it works
    with st.expander("📋 How It Works", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                ### For Candidates
                1. **Complete your profile** with target role and skills
                2. **Start interview** and answer personalized questions
                3. **Receive instant feedback** after each answer
                4. **Get detailed report** with improvement areas
                
                ### Key Features
                - Adaptive question difficulty
                - Real-time answer evaluation
                - Performance tracking
                - Personalized learning path
            """)
        
        with col2:
            st.markdown("""
                ### Tips for Success
                - ✅ Be specific and detailed
                - ✅ Include real-world examples
                - ✅ Explain concepts thoroughly
                - ✅ Practice regularly
                - ✅ Review feedback carefully
                
                ### Supported Roles
                - Software Engineering
                - Data Science
                - DevOps
                - And more...
            """)
    
    # Get Started Button
    if st.session_state.user_profile:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 START YOUR FIRST INTERVIEW", use_container_width=True):
                st.session_state.interview_active = True
                st.session_state.current_question = st.session_state.selector.select_next_question(
                    st.session_state.user_profile, []
                )
                st.rerun()
    else:
        st.info("👆 **Please complete your profile in the sidebar to begin your interview practice**")

# =============================================================================
# INTERVIEW ACTIVE SECTION
# =============================================================================
if st.session_state.interview_active:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("feedback"):
                with st.expander("📝 View Detailed Feedback", expanded=True):
                    st.markdown(message["feedback"], unsafe_allow_html=True)
    
    # Show current question
    if st.session_state.current_question:
        q = st.session_state.current_question
        
        # Display question in professional box
        st.markdown(f"""
            <div class="question-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <span style="background: #667eea; color: white; padding: 0.25rem 1rem; border-radius: 20px; font-size: 0.8rem;">
                        Question {len(st.session_state.question_history) + 1}/10
                    </span>
                    <span style="color: #64748B; font-size: 0.9rem;">
                        Difficulty: <span class="badge badge-{get_difficulty_level(q)}">{get_difficulty_level(q).title()}</span>
                    </span>
                </div>
                <div class="question-text">{q['question']}</div>
                <div class="question-meta">
                    <span>Topic: {q.get('topic', 'General').title()}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        col1, col2 = st.columns([4, 1])
        with col1:
            answer = st.text_area(
                "Your Answer:",
                height=150,
                key=f"answer_{len(st.session_state.answer_history)}",
                placeholder="Type your answer here... Be specific and provide examples when possible."
            )
        with col2:
            st.write("")
            st.write("")
            if st.button("📤 SUBMIT ANSWER", use_container_width=True, type="primary"):
                if answer:
                    # Process answer
                    with st.spinner("🤖 AI is analyzing your answer..."):
                        # Add to messages
                        st.session_state.messages.append({"role": "user", "content": answer})
                        
                        # Evaluate answer
                        feedback = st.session_state.evaluator.evaluate_answer(
                            q['id'], 
                            answer
                        )
                        
                        # Store in history
                        answer_record = {
                            "question_id": q['id'],
                            "question": q['question'],
                            "answer": answer,
                            "score": feedback["score"],
                            "topic": q.get("topic", "general"),
                            "difficulty": get_difficulty_level(q),
                            "feedback": feedback,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.answer_history.append(answer_record)
                        st.session_state.question_history.append(q['id'])
                        
                        # Update selector with performance
                        st.session_state.selector.update_performance(
                            q['id'],
                            feedback["score"],
                            q.get("topic", "general")
                        )
                        
                        # Format and display feedback
                        feedback_html = format_feedback(feedback)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "📝 **AI Feedback:**",
                            "feedback": feedback_html
                        })
                        
                        # Check if interview should continue
                        if len(st.session_state.answer_history) < 10:
                            # Select next question
                            next_q = st.session_state.selector.select_next_question(
                                st.session_state.user_profile,
                                st.session_state.answer_history
                            )
                            st.session_state.current_question = next_q
                            st.success(f"✅ Great answer! Moving to question {len(st.session_state.answer_history) + 1}/10")
                        else:
                            # Interview complete
                            st.session_state.interview_active = False
                            st.session_state.interview_complete = True
                            with st.spinner("🎯 Generating your comprehensive performance report..."):
                                st.session_state.report = st.session_state.reporter.generate_report(
                                    st.session_state.user_profile,
                                    st.session_state.answer_history
                                )
                            st.balloons()
                            st.success("🎉 Congratulations! You've completed the interview!")
                        
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning("⚠️ Please provide an answer before submitting!")
        
        # Voice input option
        with st.expander("🎤 Voice Input (Optional)"):
            st.write("Click the button and speak your answer naturally:")
            if st.button("🎤 START RECORDING", key=f"voice_{len(st.session_state.answer_history)}"):
                with st.spinner("🎤 Listening... Speak now!"):
                    voice_text = record_audio()
                    if voice_text:
                        st.success(f"✅ Recognized: {voice_text}")
                        # Set the text area value
                        st.session_state[f"answer_{len(st.session_state.answer_history)}"] = voice_text
                        st.rerun()

# =============================================================================
# INTERVIEW COMPLETE - PERFORMANCE REPORT
# =============================================================================
if st.session_state.interview_complete and st.session_state.report:
    st.balloons()
    
    # Success Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    margin: 1rem 0 2rem;
                    color: white;
                    text-align: center;">
            <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">🎉 Interview Complete!</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">Here's your comprehensive performance analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    report = st.session_state.report
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = report['summary']['overall_score']
        score_color = "#10b981" if score >= 7 else "#f59e0b" if score >= 5 else "#ef4444"
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; color: {score_color};">{score}/10</div>
                <div class="metric-label">Overall Score</div>
                <div class="badge badge-{report['summary']['performance_level']}">{report['summary']['performance_level'].title()}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; color: #667eea;">{report['summary']['total_questions']}</div>
                <div class="metric-label">Questions Answered</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; color: #667eea;">{report['summary']['completion_rate']}%</div>
                <div class="metric-label">Completion Rate</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        strengths_count = len(report['detailed_analysis']['strongest_topics'])
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; color: #667eea;">{strengths_count}</div>
                <div class="metric-label">Strength Areas</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for detailed analysis
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance Summary", "📈 Detailed Analytics", "📚 Learning Path", "🎯 Recommendations"])
    
    with tab1:
        st.subheader("📊 Topic-wise Performance")
        
        # Create DataFrame for topic performance
        topic_data = []
        for topic, data in report['detailed_analysis']['by_topic'].items():
            topic_data.append({
                "Topic": topic.title(),
                "Score": data['average_score'],
                "Questions": data['questions_attempted'],
                "Level": data['level'].title()
            })
        
        if topic_data:
            df = pd.DataFrame(topic_data)
            
            # Bar chart
            fig = px.bar(
                df,
                x='Topic',
                y='Score',
                color='Score',
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                title="Performance by Topic",
                text='Score'
            )
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0, 10]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Topic details table
            st.subheader("📋 Topic Details")
            for topic in topic_data:
                with st.expander(f"📌 {topic['Topic']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Average Score", f"{topic['Score']}/10")
                    with col2:
                        st.metric("Questions Attempted", topic['Questions'])
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Progress Over Time")
            progress_data = report['detailed_analysis']['progress_over_time']
            if progress_data:
                df_progress = pd.DataFrame(progress_data)
                fig_line = px.line(
                    df_progress,
                    x='question_number',
                    y='score',
                    title="Score Progression",
                    labels={'question_number': 'Question #', 'score': 'Score'},
                    markers=True
                )
                fig_line.update_traces(line_color='#667eea', line_width=3)
                fig_line.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_range=[0, 10]
                )
                st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            st.subheader("📊 Difficulty Analysis")
            diff_data = report['detailed_analysis']['by_difficulty']
            diff_df = pd.DataFrame([
                {
                    "Difficulty": d.title(),
                    "Score": data['average_score'],
                    "Questions": data['questions_attempted']
                }
                for d, data in diff_data.items()
            ])
            
            if not diff_df.empty:
                fig_diff = px.bar(
                    diff_df,
                    x='Difficulty',
                    y='Score',
                    color='Score',
                    color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                    title="Performance by Difficulty Level",
                    text='Score'
                )
                fig_diff.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                fig_diff.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_range=[0, 10]
                )
                st.plotly_chart(fig_diff, use_container_width=True)
        
        # Strongest and Weakest Topics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Your Strengths")
            strengths = report['detailed_analysis']['strongest_topics']
            if strengths:
                for s in strengths:
                    st.markdown(f"""
                        <div style="background: #d1fae5; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                            <strong>{s['topic'].title()}</strong>: {s['score']}/10
                            <br><small class="badge badge-{s['level']}">{s['level'].title()}</small>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Complete more questions to identify strengths")
        
        with col2:
            st.subheader("🔧 Areas for Improvement")
            weaknesses = report['detailed_analysis']['weakest_topics']
            if weaknesses:
                for w in weaknesses:
                    st.markdown(f"""
                        <div style="background: #fee2e2; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                            <strong>{w['topic'].title()}</strong>: {w['score']}/10
                            <br><small class="badge badge-{w['level']}">{w['level'].title()}</small>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Keep practicing to identify improvement areas")
    
    with tab3:
        st.subheader("📚 Your Personalized Learning Path")
        
        for phase in report['learning_path']:
            priority_color = {
                "high": "#ef4444",
                "medium": "#f59e0b",
                "low": "#10b981"
            }.get(phase['priority'], "#667eea")
            
            st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                            border-left: 4px solid {priority_color}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0;">🔹 {phase['phase'].title()} Phase</h4>
                        <span style="background: {priority_color}20; color: {priority_color}; 
                                   padding: 0.25rem 1rem; border-radius: 20px; font-size: 0.8rem;">
                            {phase['priority'].title()} Priority
                        </span>
                    </div>
                    <p style="margin: 1rem 0 0.5rem;"><strong>Focus:</strong> {phase['focus'].title()}</p>
                    <p><strong>Goal:</strong> {phase['goal']}</p>
                    <p><strong>Estimated Time:</strong> {phase['estimated_time']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Resources
        st.subheader("📖 Recommended Learning Resources")
        for resource in report.get('resources', []):
            st.markdown(f"""
                <div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <a href="{resource['url']}" target="_blank" style="text-decoration: none; color: #667eea; font-weight: 500;">
                        📘 {resource['name']}
                    </a>
                    <span style="float: right; color: #666; font-size: 0.85rem;">{resource['type'].title()}</span>
                </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("💡 Personalized Recommendations")
        
        for rec in report['recommendations']:
            st.info(rec)
        
        st.subheader("⏭️ Next Steps")
        for step in report['next_steps']:
            st.success(step)
        
        # Download Report
        st.markdown("---")
        st.subheader("📥 Download Your Report")
        
        report_json = json.dumps(report, indent=2, default=str)
        st.download_button(
            label="📥 Download Full Performance Report (JSON)",
            data=report_json,
            file_name=f"interview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        # Share options
        st.markdown("---")
        st.subheader("📤 Share Your Progress")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("📧 Email Report", use_container_width=True)
        with col2:
            st.button("📱 Share on LinkedIn", use_container_width=True)
        with col3:
            st.button("📄 Print Report", use_container_width=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p>🎯 AI Interview Coach - Professional Edition v2.0</p>
        <p style="font-size: 0.8rem;">Powered by Advanced AI Algorithms | Built with Streamlit</p>
        <p style="font-size: 0.75rem;">© 2024 All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)