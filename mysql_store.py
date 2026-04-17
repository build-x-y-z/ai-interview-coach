"""
MySQL persistence layer for authentication and interview records.
"""

import hashlib
import json
import os
import secrets
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


class MySQLStore:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", "3306"))
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DATABASE", "ai_interview_coach")
        self.enabled = os.getenv("MYSQL_ENABLED", "true").lower() == "true"

    def _connect(self, with_database: bool = True):
        config = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
        }
        if with_database:
            config["database"] = self.database
        return mysql.connector.connect(**config)

    def initialize(self) -> Tuple[bool, str]:
        if not self.enabled:
            return False, "MySQL disabled via MYSQL_ENABLED=false"
        try:
            conn = self._connect(with_database=False)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.database}`")
            cursor.close()
            conn.close()

            conn = self._connect(with_database=True)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(120) NOT NULL,
                    email VARCHAR(160) NOT NULL UNIQUE,
                    password_hash VARCHAR(64) NOT NULL,
                    password_salt VARCHAR(64) NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL UNIQUE,
                    target_role VARCHAR(120) NOT NULL,
                    experience_level VARCHAR(80) NOT NULL,
                    skills_json TEXT NOT NULL,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS interview_sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    started_at DATETIME NOT NULL,
                    ended_at DATETIME NULL,
                    total_questions INT NOT NULL DEFAULT 0,
                    overall_score DECIMAL(4,2) NULL,
                    performance_level VARCHAR(50) NULL,
                    report_json LONGTEXT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS interview_answers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    session_id INT NOT NULL,
                    question_id INT NOT NULL,
                    question_text TEXT NOT NULL,
                    answer_text LONGTEXT NOT NULL,
                    topic VARCHAR(80) NOT NULL,
                    difficulty VARCHAR(40) NOT NULL,
                    score DECIMAL(4,2) NOT NULL,
                    feedback_json LONGTEXT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES interview_sessions(id) ON DELETE CASCADE
                )
                """
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, "MySQL connection ready"
        except Exception as exc:
            return False, f"MySQL initialization failed: {exc}"

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        return hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

    def create_user(self, full_name: str, email: str, password: str) -> Tuple[bool, str]:
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (full_name, email, password_hash, password_salt)
                VALUES (%s, %s, %s, %s)
                """,
                (full_name.strip(), email.strip().lower(), password_hash, salt),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Account created successfully"
        except mysql.connector.IntegrityError:
            return False, "Email already registered"
        except Exception as exc:
            return False, f"Signup failed: {exc}"

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[Dict], str]:
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, full_name, email, password_hash, password_salt FROM users WHERE email=%s",
                (email.strip().lower(),),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if not row:
                return False, None, "No account found for this email"

            calc_hash = self._hash_password(password, row["password_salt"])
            if calc_hash != row["password_hash"]:
                return False, None, "Invalid password"

            return True, {
                "id": row["id"],
                "name": row["full_name"],
                "email": row["email"],
            }, "Login successful"
        except Exception as exc:
            return False, None, f"Login failed: {exc}"

    def get_profile(self, user_id: int) -> Optional[Dict]:
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT u.full_name, u.email, p.target_role, p.experience_level, p.skills_json
                FROM users u
                LEFT JOIN user_profiles p ON p.user_id = u.id
                WHERE u.id = %s
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if not row:
                return None

            skills = []
            if row.get("skills_json"):
                try:
                    skills = json.loads(row["skills_json"])
                except Exception:
                    skills = []

            return {
                "name": row.get("full_name") or "",
                "email": row.get("email") or "",
                "target_role": row.get("target_role") or "Software Engineer",
                "experience_level": row.get("experience_level") or "entry level",
                "skills": skills,
                "profile_complete": bool(row.get("target_role")),
            }
        except Exception:
            return None

    def save_profile(self, user_id: int, profile: Dict) -> Tuple[bool, str]:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET full_name=%s, email=%s WHERE id=%s",
                (profile.get("name", "").strip(), profile.get("email", "").strip().lower(), user_id),
            )
            cursor.execute(
                """
                INSERT INTO user_profiles (user_id, target_role, experience_level, skills_json)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  target_role=VALUES(target_role),
                  experience_level=VALUES(experience_level),
                  skills_json=VALUES(skills_json)
                """,
                (
                    user_id,
                    profile.get("target_role", "Software Engineer"),
                    profile.get("experience_level", "entry level"),
                    json.dumps(profile.get("skills", [])),
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Profile saved"
        except Exception as exc:
            return False, f"Profile save failed: {exc}"

    def create_interview_session(self, user_id: int, started_at: datetime) -> Optional[int]:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO interview_sessions (user_id, started_at)
                VALUES (%s, %s)
                """,
                (user_id, started_at.strftime("%Y-%m-%d %H:%M:%S")),
            )
            session_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            return session_id
        except Exception:
            return None

    def save_answer_record(self, session_id: int, record: Dict) -> bool:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO interview_answers (
                    session_id, question_id, question_text, answer_text,
                    topic, difficulty, score, feedback_json
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    session_id,
                    int(record.get("question_id", 0)),
                    record.get("question", ""),
                    record.get("answer", ""),
                    record.get("topic", "general"),
                    record.get("difficulty", "beginner"),
                    float(record.get("score", 0)),
                    json.dumps(record.get("feedback", {})),
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            return False

    def complete_interview_session(self, session_id: int, report: Dict) -> bool:
        try:
            summary = report.get("summary", {})
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE interview_sessions
                SET ended_at=%s,
                    total_questions=%s,
                    overall_score=%s,
                    performance_level=%s,
                    report_json=%s
                WHERE id=%s
                """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    int(summary.get("total_questions", 0)),
                    float(summary.get("overall_score", 0)),
                    summary.get("performance_level", "unknown"),
                    json.dumps(report, default=str),
                    session_id,
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            return False

    def get_recent_interviews(self, user_id: int, limit: int = 5) -> List[Dict]:
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, started_at, ended_at, total_questions, overall_score, performance_level
                FROM interview_sessions
                WHERE user_id=%s
                ORDER BY started_at DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows or []
        except Exception:
            return []
