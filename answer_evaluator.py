"""
Answer Evaluation System (Unit V)
Upgraded to use FOL predicate system.
"""

from fol_engine import FOLEngine

class AnswerEvaluator:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.fol = FOLEngine()

    def evaluate_answer(self, q_id: int, answer: str) -> dict:
        """
        Evaluate answer using FOL engine rules defining 'GoodAnswer' and 'PartialAnswer'.
        """
        question = self.kb.get_question_by_id(q_id)
        if not question:
            return {"score": 0.0, "feedback": "Question not found", "fol_trace": []}

        fol_rules = question.get("fol_rules", [])
        good_rule = next((r for r in fol_rules if r["type"] == "GoodAnswer"), None)
        partial_rule = next((r for r in fol_rules if r["type"] == "PartialAnswer"), None)
        
        good_res = self.fol.evaluate_rule(good_rule, answer) if good_rule else {"satisfied": False, "score": 0.0, "trace": []}
        part_res = self.fol.evaluate_rule(partial_rule, answer) if partial_rule else {"satisfied": False, "score": 0.0, "trace": []}
        
        # Combined score calculation
        fol_total = (good_res["score"] * 0.7) + (part_res["score"] * 0.3)
        final_score = round(fol_total * 10.0, 1) # Scale to 0-10
        
        # Combine traces
        trace = []
        if good_rule:
            trace.append("🔬 RULE: GoodAnswer Criteria")
            trace.extend(good_res["trace"])
        if partial_rule:
            trace.append("🔬 RULE: PartialAnswer Criteria")
            trace.extend(part_res["trace"])
            
        strengths = []
        weaknesses = []
        missing = []
        
        if good_res["score"] > 0.7:
            strengths.append("Answer matches the required depth and logic for this topic.")
        else:
            weaknesses.append("Missing core explanatory logic or technical details.")
            
        return {
            "score": final_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "missing_concepts": missing,
            "fol_trace": trace,
            "suggestions": ["Try to include more clear definitions and code examples where possible."],
            "feedback": f"Your logic score was {final_score}/10 based on FOL evaluation."
        }
