import sqlite3
import os
from datetime import datetime


DATABASE_PATH = os.path.join(
    "data",
    "candidates.db"
)


def initialize_database():

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_name TEXT NOT NULL,

            resume_file TEXT,

            predicted_role TEXT,

            confidence REAL DEFAULT 0,

            resume_score REAL DEFAULT 0,

            match_score REAL DEFAULT 0,

            similarity_score REAL DEFAULT 0,

            skill_score REAL DEFAULT 0,

            skills TEXT,

            matched_skills TEXT,

            missing_skills TEXT,

            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_candidate(
    candidate_name,
    resume_file,
    predicted_role,
    confidence,
    resume_score,
    match_score,
    similarity_score,
    skill_score,
    skills,
    matched_skills,
    missing_skills
):

    initialize_database()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO candidates (

            candidate_name,
            resume_file,
            predicted_role,
            confidence,
            resume_score,
            match_score,
            similarity_score,
            skill_score,
            skills,
            matched_skills,
            missing_skills,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        candidate_name,
        resume_file,
        predicted_role,
        confidence,
        resume_score,
        match_score,
        similarity_score,
        skill_score,

        ", ".join(skills)
        if isinstance(skills, list)
        else str(skills),

        ", ".join(matched_skills)
        if isinstance(matched_skills, list)
        else str(matched_skills),

        ", ".join(missing_skills)
        if isinstance(missing_skills, list)
        else str(missing_skills),

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()

    candidate_id = cursor.lastrowid

    connection.close()

    return candidate_id


def get_all_candidates():

    initialize_database()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        ORDER BY match_score DESC
    """)

    candidates = cursor.fetchall()

    connection.close()

    return candidates


def search_candidates(keyword):

    initialize_database()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT *
        FROM candidates

        WHERE
            candidate_name LIKE ?
            OR predicted_role LIKE ?
            OR skills LIKE ?

        ORDER BY match_score DESC
    """, (
        search_value,
        search_value,
        search_value
    ))

    candidates = cursor.fetchall()

    connection.close()

    return candidates


def get_candidate(candidate_id):

    initialize_database()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        WHERE id = ?
    """, (
        candidate_id,
    ))

    candidate = cursor.fetchone()

    connection.close()

    return candidate


def delete_candidate(candidate_id):

    initialize_database()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM candidates
        WHERE id = ?
    """, (
        candidate_id,
    ))

    connection.commit()

    connection.close()


def get_statistics():

    initialize_database()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM candidates
    """)

    total_candidates = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(match_score)
        FROM candidates
    """)

    average_match = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM candidates
        WHERE match_score >= 70
    """)

    shortlisted = cursor.fetchone()[0]

    connection.close()

    return {
        "total_candidates": total_candidates,
        "average_match": round(
            average_match or 0,
            2
        ),
        "shortlisted": shortlisted
    }


if __name__ == "__main__":

    initialize_database()

    print(
        "Candidate database initialized successfully."
    )

    print(
        f"Database location: {DATABASE_PATH}"
    )