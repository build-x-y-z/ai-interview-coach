"""
Intelligent Question Selection using Informed Search (Unit III)
Implements Best-First Search with heuristics
"""

import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

class QuestionSelector:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.question_history = []  # Stores IDs of questions already asked
        self.performance_history = []
        self.difficulty_scores = {"beginner": 1, "intermediate": 2, "advanced": 3}
        
    def select_next_question(self, user_profile: Dict, previous_answers: List[Dict]) -> Optional[Dict]:
        """
        Select next question using heuristic search (Best-First Search approach)
        """
        candidate_questions = self._get_candidate_questions(user_profile)
        
        available_questions = []
        for q in candidate_questions:
            q_id = q.get('id')
            if q_id and q_id not in self.question_history:
                available_questions.append(q)
        
        if not available_questions:
            return None
        
        scored_questions = []
        for q in available_questions:
            score = self._calculate_heuristic(q, user_profile, previous_answers)
            scored_questions.append((score, q))
        
        scored_questions.sort(key=lambda x: x[0], reverse=True)
        
        if scored_questions:
            selected = scored_questions[0][1].copy()
            
            try:
                import streamlit as st
                if st.session_state.get('ai_enhanced_mode', False):
                    from utils import call_gemini
                    
                    topic = str(selected.get("topic", "general"))
                    difficulty = str(selected.get("difficulty", "intermediate"))
                    role = str(user_profile.get("target_role", "candidate"))
                    concepts = selected.get("concepts", [])
                    top_concept = str(concepts[0]) if (concepts and len(concepts) > 0) else topic
                    
                    prompt = (
                        f"You are a technical interviewer. Generate exactly ONE interview question "
                        f"about {topic} at {difficulty} level for a {role} candidate.\n"
                        f"The question must test understanding of {top_concept}.\n"
                        f"Return ONLY the question text. No numbering, no explanation, no quotes.\n"
                        f"Maximum 25 words."
                    )
                    
                    llm_question = call_gemini(prompt, feature_name="Feature 4: Dynamic Question")
                    if llm_question:
                        selected["question"] = llm_question
            except Exception:
                pass
                
            if selected.get('id'):
                self.question_history.append(selected['id'])
            return selected
        
        return None
    
    def _calculate_heuristic(self, question: Dict, profile: Dict, previous_answers: List[Dict]) -> float:
        w1, w2, w3, w4 = 0.3, 0.3, 0.2, 0.2
        relevance = self._calculate_relevance(question, profile)
        difficulty_match = self._calculate_difficulty_match(question, profile)
        novelty = self._calculate_novelty(question)
        weakness_focus = self._calculate_weakness_focus(question, previous_answers)
        return float(w1 * relevance + w2 * difficulty_match + w3 * novelty + w4 * weakness_focus)
    
    def _calculate_relevance(self, question: Dict, profile: Dict) -> float:
        target_role = str(profile.get("target_role", "")).lower()
        role_topics = {
            "software engineer": ["python", "dsa", "algorithms"],
            "data scientist": ["python", "sql", "machine learning"],
            "backend developer": ["python", "sql", "java"]
        }
        question_topic = str(question.get("topic", "")).lower()
        for role in role_topics:
            if role in target_role:
                if question_topic in role_topics[role]:
                    return 1.0
        return 0.5
    
    def _calculate_difficulty_match(self, question: Dict, profile: Dict) -> float:
        user_level = str(profile.get("experience_level", "entry")).lower()
        if "entry" in user_level: u_lvl = "beginner"
        elif "mid" in user_level: u_lvl = "intermediate"
        else: u_lvl = "advanced"
        
        q_lvl = str(question.get("difficulty") or "beginner").lower()
        diff_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
        u_val = diff_map.get(u_lvl, 1)
        q_val = diff_map.get(q_lvl, 1)
        
        dist = abs(u_val - q_val)
        if dist == 0: return 1.0
        if dist == 1: return 0.7
        return 0.3
    
    def _calculate_novelty(self, question: Dict) -> float:
        q_id = question.get("id")
        h_len = len(self.question_history)
        if q_id in self.question_history: return 0.0
        
        # Avoid indexing into list slices to satisfy linters
        for i in range(max(0, h_len - 5), h_len):
            if self.question_history[i] == q_id: return 0.3
        return 1.0
    
    def _calculate_weakness_focus(self, question: Dict, previous_answers: List[Dict]) -> float:
        if not previous_answers: return 0.5
        q_topic = str(question.get("topic", "")).lower()
        latest_score = 5.0
        found = False
        for i in range(len(previous_answers)-1, -1, -1):
            ans = previous_answers[i]
            if str(ans.get("topic", "")).lower() == q_topic:
                latest_score = float(ans.get("score", 5.0))
                found = True
                break
        if not found: return 0.5
        focus = 1.0 - (latest_score / 10.0)
        return float(max(0.0, min(1.0, focus)))
            
    def get_predicted_questions(self, user_profile: Dict, previous_answers: List[Dict], n: int = 3) -> List[Tuple[float, Dict]]:
        candidates = self._get_candidate_questions(user_profile)
        available = [q for q in candidates if q.get('id') not in self.question_history]
        if not available: return []
        scored = []
        for q in available:
            score = self._calculate_heuristic(q, user_profile, previous_answers)
            scored.append((score, q))
        scored.sort(key=lambda x: x[0], reverse=True)
        res = []
        for i in range(min(len(scored), n)):
            res.append(scored[i])
        return res
    
    def _get_candidate_questions(self, profile: Dict) -> List[Dict]:
        candidates = []
        chosen_skills = [s.lower() for s in profile.get("skills", [])]
        
        # Only pull from KB for topics in chosen_skills
        for skill in chosen_skills:
            for lvl in ["beginner", "intermediate", "advanced"]:
                qs = self.kb.get_questions_by_topic(skill, lvl)
                if qs:
                    for q in qs:
                        if q.get('id') not in self.question_history:
                            candidates.append(q)
                            
        # Deduplicate
        unique = []
        seen = set()
        for q in candidates:
            qid = q.get('id')
            if qid not in seen:
                seen.add(qid)
                unique.append(q)
        return unique
    
    def update_performance(self, question_id: int, score: float, topic: str):
        self.performance_history.append({
            "q_id": question_id, "score": float(score), "topic": topic,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def reset_history(self):
        self.question_history = []
        self.performance_history = []
