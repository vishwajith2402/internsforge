import re


SKILL_DATABASE = {

    # Programming
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "r programming",
    "php",
    "go",
    "rust",

    # Data Science / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "natural language processing",
    "nlp",
    "computer vision",
    "predictive modeling",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",
    "opencv",

    # Python libraries
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "plotly",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "oracle",
    "redis",

    # Cloud
    "aws",
    "amazon web services",
    "azure",
    "google cloud",
    "gcp",

    # DevOps
    "docker",
    "kubernetes",
    "git",
    "github",
    "gitlab",
    "jenkins",

    # Web
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "nodejs",
    "express",

    # BI
    "power bi",
    "tableau",
    "excel",

    # Other
    "rest api",
    "api",
    "linux",
    "streamlit",
    "flask",
    "django",
    "fastapi"
}


def normalize_text(text):
    """Normalize text for skill matching."""

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def extract_skills(text):
    """Extract known technical skills."""

    text = normalize_text(
        text
    )

    found_skills = []

    for skill in SKILL_DATABASE:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(
            pattern,
            text
        ):

            found_skills.append(
                skill
            )

    return sorted(
        set(found_skills)
    )


def extract_skills_text(text):
    """Return skills as comma-separated text."""

    skills = extract_skills(
        text
    )

    return ", ".join(
        skills
    )


if __name__ == "__main__":

    sample = """
    I am a Python developer with experience
    in Machine Learning, Pandas, NumPy,
    SQL, TensorFlow, Docker and AWS.
    """

    skills = extract_skills(
        sample
    )

    print(
        "Detected Skills:"
    )

    for skill in skills:

        print(
            "-",
            skill
        )