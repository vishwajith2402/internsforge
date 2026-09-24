import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skill_extractor import extract_skills


def clean_text(text):
    """Basic text cleaning."""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def calculate_similarity(
    resume_text,
    job_description
):
    """Calculate TF-IDF cosine similarity."""

    resume = clean_text(
        resume_text
    )

    job = clean_text(
        job_description
    )

    if not resume or not job:

        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(
        [resume, job]
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return float(
        similarity * 100
    )


def calculate_skill_match(
    resume_text,
    job_description
):
    """Calculate skill overlap."""

    resume_skills = set(
        extract_skills(
            resume_text
        )
    )

    required_skills = set(
        extract_skills(
            job_description
        )
    )

    if not required_skills:

        return {
            "resume_skills": sorted(
                resume_skills
            ),
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "skill_score": 0.0
        }

    matched = (
        resume_skills &
        required_skills
    )

    missing = (
        required_skills -
        resume_skills
    )

    score = (
        len(matched) /
        len(required_skills)
    ) * 100

    return {
        "resume_skills": sorted(
            resume_skills
        ),
        "required_skills": sorted(
            required_skills
        ),
        "matched_skills": sorted(
            matched
        ),
        "missing_skills": sorted(
            missing
        ),
        "skill_score": round(
            score,
            2
        )
    }


def calculate_match(
    resume_text,
    job_description
):
    """Generate complete job match analysis."""

    similarity = calculate_similarity(
        resume_text,
        job_description
    )

    skill_data = calculate_skill_match(
        resume_text,
        job_description
    )

    skill_score = skill_data[
        "skill_score"
    ]

    # Combined score
    overall_score = (
        (similarity * 0.5)
        +
        (skill_score * 0.5)
    )

    return {
        "similarity_score": round(
            similarity,
            2
        ),

        "skill_score": round(
            skill_score,
            2
        ),

        "overall_score": round(
            overall_score,
            2
        ),

        "resume_skills":
            skill_data[
                "resume_skills"
            ],

        "required_skills":
            skill_data[
                "required_skills"
            ],

        "matched_skills":
            skill_data[
                "matched_skills"
            ],

        "missing_skills":
            skill_data[
                "missing_skills"
            ]
    }


if __name__ == "__main__":

    resume = """
    Python developer with experience in
    machine learning, pandas, numpy,
    SQL and scikit-learn.
    """

    job = """
    We are looking for a Machine Learning
    Engineer with Python, machine learning,
    SQL, Docker, AWS and TensorFlow.
    """

    result = calculate_match(
        resume,
        job
    )

    print("=" * 60)
    print("JOB MATCH TEST")
    print("=" * 60)

    print(
        "Similarity:",
        result["similarity_score"],
        "%"
    )

    print(
        "Skill Match:",
        result["skill_score"],
        "%"
    )

    print(
        "Overall Match:",
        result["overall_score"],
        "%"
    )

    print(
        "\nMatched Skills:"
    )

    for skill in result["matched_skills"]:

        print(
            "✓",
            skill
        )

    print(
        "\nMissing Skills:"
    )

    for skill in result["missing_skills"]:

        print(
            "✗",
            skill
        )