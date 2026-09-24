import os

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from job_matcher import calculate_match


SUPPORTED_FILES = (
    ".pdf",
    ".docx",
    ".txt"
)


def process_resume(
    file_path,
    job_description
):

    result = {

        "file": os.path.basename(
            file_path
        ),

        "path": file_path,

        "success": False,

        "error": None
    }

    try:

        text = extract_resume_text(
            file_path
        )

        if not text.strip():

            raise ValueError(
                "No readable text found."
            )

        skills = extract_skills(
            text
        )

        match_result = calculate_match(
            text,
            job_description
        )

        result.update({

            "text": text,

            "skills": skills,

            "match": match_result,

            "success": True
        })

    except Exception as error:

        result["error"] = str(
            error
        )

    return result


def process_folder(
    folder_path,
    job_description
):

    results = []

    if not os.path.isdir(
        folder_path
    ):

        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    files = os.listdir(
        folder_path
    )

    resume_files = [

        filename

        for filename in files

        if filename.lower().endswith(
            SUPPORTED_FILES
        )
    ]

    for filename in resume_files:

        file_path = os.path.join(
            folder_path,
            filename
        )

        result = process_resume(
            file_path,
            job_description
        )

        results.append(
            result
        )

    return results


def get_successful_results(
    results
):

    return [

        result

        for result in results

        if result.get("success")
    ]


def get_failed_results(
    results
):

    return [

        result

        for result in results

        if not result.get("success")
    ]


if __name__ == "__main__":

    print(
        "Batch Resume Processor"
    )

    print(
        "Module loaded successfully."
    )

    print(
        "Supported formats:",
        ", ".join(
            SUPPORTED_FILES
        )
    )