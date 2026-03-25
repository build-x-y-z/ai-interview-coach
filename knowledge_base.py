"""
Knowledge Base System (Unit I & V)
Stores questions, answers, and evaluation criteria with FOL Rules
"""

import json
from typing import List, Dict, Any

class KnowledgeBase:
    def __init__(self):
        self.questions = self._initialize_questions()
        self.skill_topics = self._initialize_topics()
        self.ideal_answers = self._initialize_ideal_answers()
    
    def _initialize_questions(self) -> Dict:
        """Initialize question bank with categories, difficulty levels and FOL rules"""
        return {
            "python": {
                "beginner": [
                    {
                        "id": 1,
                        "question": "What is a list in Python? Explain with example.",
                        "topic": "python",
                        "difficulty": "beginner",
                        "keywords": ["mutable", "ordered", "sequence", "collection", "[]"],
                        "concepts": ["mutable", "indexing", "slicing"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["mutable"]},
                                    {"fn": "Explains", "args": ["indexing"]},
                                    {"fn": "ExemplifiesCode", "args": []},
                                    {"fn": "IsDetailed", "args": [25]}
                                ],
                                "connective": "AND", "weight": 1.0
                            },
                            {
                                "type": "PartialAnswer", 
                                "predicates": [
                                    {"fn": "Contains", "args": ["list"]},
                                    {"fn": "IsDetailed", "args": [10]}
                                ],
                                "connective": "AND", "weight": 0.5
                            }
                        ]
                    },
                    {
                        "id": 2,
                        "question": "What is the difference between tuple and list?",
                        "topic": "python",
                        "difficulty": "beginner",
                        "keywords": ["immutable", "mutable", "faster", "parentheses", "brackets"],
                        "concepts": ["immutability", "performance", "syntax"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["immutable"]},
                                    {"fn": "Defines", "args": ["tuple"]},
                                    {"fn": "IsDetailed", "args": [30]}
                                ],
                                "connective": "AND", "weight": 1.0
                            }
                        ]
                    }
                ],
                "intermediate": [
                    {
                        "id": 4,
                        "question": "Explain decorators in Python with example.",
                        "topic": "python",
                        "difficulty": "intermediate",
                        "keywords": ["@", "wrapper", "function", "modify", "behavior"],
                        "concepts": ["higher-order functions", "metaprogramming"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["@"]},
                                    {"fn": "Explains", "args": ["wrapper"]},
                                    {"fn": "ExemplifiesCode", "args": []}
                                ],
                                "connective": "AND", "weight": 1.0
                            }
                        ]
                    }
                ],
                "advanced": [
                    {
                        "id": 6,
                        "question": "Explain generators and yield keyword.",
                        "topic": "python",
                        "difficulty": "advanced",
                        "keywords": ["iterator", "lazy", "memory", "yield", "state"],
                        "concepts": ["lazy evaluation", "iteration protocol"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["yield"]},
                                    {"fn": "Explains", "args": ["lazy"]},
                                    {"fn": "IsDetailed", "args": [40]}
                                ],
                                "connective": "AND", "weight": 1.0
                            }
                        ]
                    }
                ]
            },
            "sql": {
                "beginner": [
                    {
                        "id": 7,
                        "question": "What is SQL and what are its main types of commands?",
                        "topic": "sql",
                        "difficulty": "beginner",
                        "keywords": ["database", "DDL", "DML", "DCL", "query"],
                        "concepts": ["data definition", "data manipulation"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["DDL"]},
                                    {"fn": "Contains", "args": ["DML"]},
                                    {"fn": "IsDetailed", "args": [20]}
                                ],
                                "connective": "AND", "weight": 1.0
                            }
                        ]
                    }
                ]
            },
            "java": {
                "beginner": [
                    {
                        "id": 201,
                        "question": "What is JVM and how does it provide platform independence?",
                        "topic": "java",
                        "difficulty": "beginner",
                        "keywords": ["Virtual Machine", "bytecode", "compiled", "platform"],
                        "concepts": ["JVM architecture", "platform independence"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["bytecode"]},
                                    {"fn": "Explains", "args": ["JVM"]},
                                    {"fn": "IsDetailed", "args": [30]}
                                ],
                                "connective": "AND", "weight": 1.0
                            }
                        ]
                    },
                    {
                        "id": 202,
                        "question": "What are the core principles of OOP in Java?",
                        "topic": "java",
                        "difficulty": "beginner",
                        "keywords": ["encapsulation", "inheritance", "polymorphism", "abstraction"],
                        "concepts": ["OOP principles", "Object interaction"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["inheritance"]},
                                    {"fn": "Contains", "args": ["polymorphism"]},
                                    {"fn": "IsDetailed", "args": [35]}
                                ],
                                "connective": "AND", "weight": 1.0
                            }
                        ]
                    }
                ]
            },
            "dsa": {
                "beginner": [
                    {
                        "id": 301,
                        "question": "What is Big O notation and why is it important?",
                        "topic": "dsa",
                        "difficulty": "beginner",
                        "keywords": ["complexity", "time", "space", "scaling", "asymptotic"],
                        "concepts": ["algorithm analysis", "performance scaling"],
                        "fol_rules": [
                            {
                                "type": "GoodAnswer",
                                "predicates": [
                                    {"fn": "Contains", "args": ["complexity"]},
                                    {"fn": "Explains", "args": ["scaling"]},
                                    {"fn": "IsDetailed", "args": [25]}
                                ],
                                "connective": "AND", "weight": 1.0
                            }
                        ]
                    }
                ]
            }
        }
    
    def _initialize_topics(self) -> Dict:
        return {
            "python": {"prerequisites": [], "core_topics": ["basics"]},
            "sql": {"prerequisites": [], "core_topics": ["queries"]},
            "java": {"prerequisites": [], "core_topics": ["JVM", "OOP"]},
            "dsa": {"prerequisites": [], "core_topics": ["Big O"]}
        }
    
    def _initialize_ideal_answers(self) -> Dict:
        return {
            1: {"key_points": ["Mutable", "Ordered"], "example": "[]"},
            201: {"key_points": ["Bytecode", "Write once run anywhere"], "example": "java MyClass.class"},
            301: {"key_points": ["Asymptotic notation", "Performance measurement"], "example": "O(n)"}
        }

    def get_all_questions(self) -> List:
        res = []
        for topic in self.questions:
            for level in self.questions[topic]:
                res.extend(self.questions[topic][level])
        return res

    def get_questions_by_topic(self, topic: str, level: str) -> List:
        t_key = topic.lower()
        if t_key in self.questions:
            return self.questions[t_key].get(level.lower(), [])
        return []

    def get_question_by_id(self, q_id: int) -> Dict:
        for q in self.get_all_questions():
            if q["id"] == q_id or str(q["id"]) == str(q_id):
                return q
        return None

    def explore_topics_bfs(self) -> List[Dict]:
        """Unit II: BFS Tree traversal representation"""
        nodes = []
        for topic in self.questions:
            nodes.append({"name": topic.upper(), "level": "topic"})
            for diff in self.questions[topic]:
                nodes.append({"name": diff.capitalize(), "level": "difficulty"})
                for q in self.questions[topic][diff]:
                    nodes.append({"name": q["question"], "id": q["id"], "level": "question"})
        return nodes
