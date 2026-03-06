"""
Utility functions for the AI Interview Coach
Handles helper functions, formatting, and voice features
"""

import streamlit as st
import json
import re
from datetime import datetime
import random
import base64
from typing import List, Dict, Any, Optional

# Try to import voice libraries (optional)
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

# =============================================================================
# ANIMATION FUNCTIONS
# =============================================================================

def get_typing_animation():
    """Returns CSS for typing animation"""
    return """
    <style>
    .typing-indicator {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    .typing-indicator span {
        height: 10px;
        width: 10px;
        background: #667eea;
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: typing 1.5s infinite ease-in-out;
    }
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes typing {
        0% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .rotate {
        animation: rotate 2s linear infinite;
    }
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .float {
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .glow {
        animation: glow 2s ease-in-out infinite;
    }
    @keyframes glow {
        0% { box-shadow: 0 0 5px #667eea; }
        50% { box-shadow: 0 0 20px #667eea; }
        100% { box-shadow: 0 0 5px #667eea; }
    }
    
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .bounce {
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    </style>
    """

def get_confetti_animation():
    """Returns JavaScript for confetti animation"""
    return """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
    <script>
    function launchConfetti() {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    }
    function launchBigConfetti() {
        confetti({
            particleCount: 150,
            spread: 100,
            origin: { y: 0.6 }
        });
        confetti({
            particleCount: 150,
            spread: 100,
            origin: { y: 0.6, x: 0.2 }
        });
        confetti({
            particleCount: 150,
            spread: 100,
            origin: { y: 0.6, x: 0.8 }
        });
    }
    </script>
    """

def get_robot_avatar(emotion="neutral"):
    """Returns robot avatar HTML with different emotions"""
    avatars = {
        "neutral": """
            <svg width="100" height="100" viewBox="0 0 100 100" class="float">
                <circle cx="50" cy="50" r="40" fill="#667eea" opacity="0.2"/>
                <circle cx="35" cy="40" r="5" fill="#667eea"/>
                <circle cx="65" cy="40" r="5" fill="#667eea"/>
                <path d="M35 60 Q50 70 65 60" stroke="#667eea" stroke-width="3" fill="none"/>
                <rect x="45" y="20" width="10" height="15" fill="#667eea" opacity="0.3"/>
            </svg>
        """,
        "happy": """
            <svg width="100" height="100" viewBox="0 0 100 100" class="bounce">
                <circle cx="50" cy="50" r="40" fill="#10b981" opacity="0.2"/>
                <circle cx="35" cy="40" r="5" fill="#10b981"/>
                <circle cx="65" cy="40" r="5" fill="#10b981"/>
                <path d="M35 60 Q50 75 65 60" stroke="#10b981" stroke-width="3" fill="none"/>
                <rect x="45" y="20" width="10" height="15" fill="#10b981" opacity="0.3"/>
            </svg>
        """,
        "thinking": """
            <svg width="100" height="100" viewBox="0 0 100 100" class="rotate" style="animation-duration: 3s;">
                <circle cx="50" cy="50" r="40" fill="#f59e0b" opacity="0.2"/>
                <circle cx="35" cy="40" r="5" fill="#f59e0b"/>
                <circle cx="65" cy="40" r="5" fill="#f59e0b"/>
                <circle cx="50" cy="60" r="3" fill="#f59e0b"/>
                <rect x="45" y="20" width="10" height="15" fill="#f59e0b" opacity="0.3"/>
                <circle cx="80" cy="20" r="8" fill="#f59e0b" opacity="0.2">
                    <animate attributeName="r" values="8;12;8" dur="1s" repeatCount="indefinite"/>
                </circle>
            </svg>
        """
    }
    return avatars.get(emotion, avatars["neutral"])

def get_loading_spinner():
    """Returns loading spinner HTML"""
    return """
    <div style="display: flex; justify-content: center; align-items: center; margin: 20px 0;">
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    """

def get_progress_ring(percentage, size=100):
    """Returns a progress ring SVG"""
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" fill="none" stroke="#e2e8f0" stroke-width="8"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="#667eea" stroke-width="8"
                stroke-dasharray="251.2" 
                stroke-dashoffset="{251.2 - (251.2 * percentage / 100)}"
                transform="rotate(-90 50 50)">
            <animate attributeName="stroke-dashoffset" 
                     values="{251.2};{251.2 - (251.2 * percentage / 100)}" 
                     dur="1s" fill="freeze"/>
        </circle>
        <text x="50" y="55" text-anchor="middle" fill="#667eea" font-size="20" font-weight="bold">
            {percentage}%
        </text>
    </svg>
    """

# =============================================================================
# ORIGINAL UTILITY FUNCTIONS
# =============================================================================

def get_difficulty_level(question):
    """Extract difficulty level from question"""
    if isinstance(question, dict):
        # Check multiple possible keys for difficulty
        difficulty = question.get('difficulty_level') or question.get('difficulty') or 'beginner'
        return difficulty
    return 'beginner'

def format_feedback(feedback):
    """Format feedback for display with animations"""
    score = feedback.get('score', 0)
    if score >= 7:
        score_class = "score-high"
        icon = "🎉"
    elif score >= 5:
        score_class = "score-medium"
        icon = "📊"
    else:
        score_class = "score-low"
        icon = "💪"
    
    html = f"""
    <div class="feedback-box fade-in">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <h4 style="margin: 0;">{icon} Score: <span class="{score_class}">{feedback['score']}/10</span></h4>
            <div class="glow" style="width: 40px; height: 40px; border-radius: 50%; background: #667eea20;"></div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
            <div style="background: #d1fae5; padding: 1rem; border-radius: 10px;" class="slide-in">
                <h5 style="color: #065f46; margin: 0 0 0.5rem 0;">✅ Strengths:</h5>
                <ul style="margin: 0; padding-left: 1.2rem;">
    """
    
    for strength in feedback.get('strengths', []):
        html += f"<li style='color: #065f46;'>{strength}</li>"
    
    html += """
                </ul>
            </div>
            
            <div style="background: #fee2e2; padding: 1rem; border-radius: 10px;" class="slide-in">
                <h5 style="color: #991b1b; margin: 0 0 0.5rem 0;">🔧 Areas to Improve:</h5>
                <ul style="margin: 0; padding-left: 1.2rem;">
    """
    
    for weakness in feedback.get('weaknesses', []):
        html += f"<li style='color: #991b1b;'>{weakness}</li>"
    
    html += """
                </ul>
            </div>
        </div>
        
        <div style="background: #e0e7ff; padding: 1rem; border-radius: 10px; margin: 1rem 0;" class="fade-in">
            <h5 style="color: #1e40af; margin: 0 0 0.5rem 0;">💡 Suggestions:</h5>
            <ul style="margin: 0; padding-left: 1.2rem;">
    """
    
    for suggestion in feedback.get('suggestions', []):
        html += f"<li style='color: #1e40af;'>{suggestion}</li>"
    
    html += """
            </ul>
        </div>
        
        <div style="background: #f3e8ff; padding: 1rem; border-radius: 10px;" class="fade-in">
            <h5 style="color: #6b21a8; margin: 0 0 0.5rem 0;">📝 Ideal Answer Should Include:</h5>
            <ul style="margin: 0; padding-left: 1.2rem;">
    """
    
    for point in feedback.get('ideal_answer', {}).get('key_points', []):
        html += f"<li style='color: #6b21a8;'>{point}</li>"
    
    html += """
            </ul>
    """
    
    if feedback.get('ideal_answer', {}).get('example'):
        html += f"""
            <div style="background: #1e293b; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <pre style="color: #a5f3fc; margin: 0; font-family: 'Courier New', monospace;"><code>{feedback['ideal_answer']['example']}</code></pre>
            </div>
        """
    
    html += """
        </div>
    </div>
    """
    
    return html

def record_audio():
    """Record audio and convert to text"""
    if not VOICE_AVAILABLE:
        st.warning("Voice input is not available. Please install required packages: pip install speechrecognition pyttsx3 PyAudio")
        return None
    
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            with st.spinner("🎤 Listening... Speak now!"):
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=30)
        
        with st.spinner("🔄 Processing your speech..."):
            text = recognizer.recognize_google(audio)
            return text
    
    except sr.WaitTimeoutError:
        st.error("No speech detected. Please try again.")
        return None
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        st.error("Speech recognition service error. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def text_to_speech(text):
    """Convert text to speech"""
    if not VOICE_AVAILABLE:
        return
    
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")

def save_interview_session(session_data, filename=None):
    """Save interview session to file"""
    if filename is None:
        filename = f"interview_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(session_data, f, indent=2)
    
    return filename

def load_interview_session(filename):
    """Load interview session from file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading session: {str(e)}")
        return None

def calculate_similarity(text1, text2):
    """Calculate simple similarity between two texts"""
    # Convert to lowercase and split into words
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    
    if not words1 or not words2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0

def extract_keywords(text):
    """Extract important keywords from text"""
    # Simple keyword extraction - can be improved with NLP
    words = re.findall(r'\w+', text.lower())
    
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                  'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should',
                  'may', 'might', 'must', 'can', 'could', 'this', 'that', 'these',
                  'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
                  'his', 'her', 'its', 'our', 'their'}
    
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count frequencies
    freq = {}
    for word in keywords:
        freq[word] = freq.get(word, 0) + 1
    
    # Return top keywords
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:10]]

def generate_question_id():
    """Generate unique question ID"""
    return f"Q{random.randint(1000, 9999)}"

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_time(seconds):
    """Format seconds into readable time"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def create_progress_chart(scores):
    """Create a progress chart"""
    fig = {
        "data": [
            {
                "type": "scatter",
                "x": list(range(1, len(scores) + 1)),
                "y": scores,
                "mode": "lines+markers",
                "name": "Score Progression",
                "line": {"color": "#1E88E5", "width": 3},
                "marker": {"size": 10}
            }
        ],
        "layout": {
            "title": "Your Performance Trend",
            "xaxis": {"title": "Question Number"},
            "yaxis": {"title": "Score", "range": [0, 10]},
            "showlegend": False
        }
    }
    return fig

def get_welcome_animation():
    """Returns welcome animation HTML"""
    return """
    <div style="text-align: center; padding: 2rem;">
        <div class="float" style="font-size: 5rem;">🎯</div>
        <h1 class="pulse" style="color: #667eea;">Welcome to AI Interview Coach</h1>
        <div class="typing-indicator" style="justify-content: center;">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    """

def get_success_animation():
    """Returns success animation HTML"""
    return """
    <div style="text-align: center; padding: 1rem;">
        <div class="bounce" style="font-size: 3rem;">✅</div>
        <div class="glow" style="width: 100%; height: 4px; background: #10b981; border-radius: 2px; margin: 1rem 0;">
            <div style="width: 100%; height: 100%; background: #10b981; border-radius: 2px;" class="pulse"></div>
        </div>
    </div>
    """