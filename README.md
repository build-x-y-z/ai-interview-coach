# 🎯 AI Interview Coach — Professional Edition v3.0

An intelligent, real-time interview preparation system that simulates a live video call. It uses Artificial Intelligence to conduct mock interviews, featuring live video self-view, actual AI voice synthesis, speech-to-text answering, and personalized evaluation reporting.

## ✨ Key Features

### 🎥 Live Video & Voice Experience
- **Browser-Native Self-View**: See yourself during the interview via a seamless `getUserMedia()` video feed (just like Google Meet/Zoom), operating entirely in-browser with zero latency.
- **AI Voice Coaching**: The AI interviewer speaks its greetings and questions aloud using cached Text-to-Speech (gTTS) for uninterrupted playback.
- **Voice Recognition Answers**: Simply click "Unmute" and verbally answer the questions. The system records and accurately transcribes your speech.

### 🧠 Core Engine Capabilities
- **Personalized Interviews**: Questions adapt dynamically to your target role (e.g., Software Engineer, Data Scientist) and experience level.
- **Heuristic Question Selection**: Uses Best-First Search to ensure questions cover diverse topics, adapt to your difficulty level, and avoid repetition.
- **Instant Logic-Based Evaluation**: Answer evaluation powered by Forward Chaining logic rules that scan for exact keywords, underlying concepts, and logical completeness.
- **Comprehensive Analytics**: A final Wrap-Up report that details your overall score, topic-wise strengths/weaknesses, and gives an actionable learning path.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Microphone and Webcam 

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-interview-coach.git
   cd ai-interview-coach
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   # Or use the provided batch script on Windows:
   # .\run.bat
   ```

4. **Access the App**
   Open your browser to `http://localhost:8501`. **Allow Camera and Microphone permissions** when prompted.

---

## 🛠️ Technology Stack

**Frontend / Interface:**
- **Framework**: Streamlit
- **Media**: Streamlit `components.v1.html` (for direct DOM Video access)
- **UI State**: Streamlit Session State for seamless multi-stage rendering

**Audio & Voice Processing:**
- **Text-to-Speech**: `gTTS` (Google Text-to-Speech) with session-state base64 caching.
- **Speech-to-Text**: `speech_recognition` & `audio_recorder_streamlit`.

**AI & Backend Logic:**
- **Search Algorithms**: Best-First Search (Question Selection).
- **Inference Engine**: Forward Chaining (Answer Evaluation). 

---

## 📖 Usage Guide

1. **Profile Setup**: In the left sidebar, enter your role, experience, and key skills. Click "Save Profile".
2. **Start the Meeting**: Click **Start Your Interview**. The camera feed connects, and the AI introduces the session.
3. **The Interview**: Click "I'm Ready" to begin. The AI will speak each question out loud. Look into your camera, click the microphone button, and dictate your answer.
4. **The Evaluation**: After 10 questions, the interview concludes automatically, generating your comprehensive performance report.

---
*Built to help candidates practice technical interviews in a highly realistic, pressured environment.*
