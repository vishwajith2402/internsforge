def calculate_candidate_score(
    match_score,
    resume_score,
    confidence
):
    """
    Calculate the final candidate ranking score.

    Weight:
        Job Match       = 60%
        Resume Quality  = 25%
        ML Confidence   = 15%
    """

    match_score = float(
        match_score or 0
    )

    resume_score = float(
        resume_score or 0
    )

    confidence = float(
        confidence or 0
    )

    final_score = (
        (match_score * 0.60)
        +
        (resume_score * 0.25)
        +
        (confidence * 0.15)
    )

    return round(
        final_score,
        2
    )


def rank_candidates(candidates):

    ranked_candidates = []

    for candidate in candidates:

        final_score = calculate_candidate_score(
            candidate["match_score"],
            candidate["resume_score"],
            candidate["confidence"]
        )

        ranked_candidates.append({

            "id": candidate["id"],

            "name": candidate[
                "candidate_name"
            ],

            "role": candidate[
                "predicted_role"
            ],

            "match_score": candidate[
                "match_score"
            ],

            "resume_score": candidate[
                "resume_score"
            ],

            "confidence": candidate[
                "confidence"
            ],

            "ranking_score": final_score
        })

    ranked_candidates.sort(
        key=lambda candidate:
            candidate["ranking_score"],
        reverse=True
    )

    return ranked_candidates


def get_rank_label(rank):

    if rank == 1:
        return "🥇"

    if rank == 2:
        return "🥈"

    if rank == 3:
        return "🥉"

    return str(rank)


if __name__ == "__main__":

    sample_candidates = [

        {
            "id": 1,
            "candidate_name": "Candidate A",
            "predicted_role": "Data Scientist",
            "match_score": 92,
            "resume_score": 88,
            "confidence": 94
        },

        {
            "id": 2,
            "candidate_name": "Candidate B",
            "predicted_role": "ML Engineer",
            "match_score": 85,
            "resume_score": 91,
            "confidence": 89
        }
    ]

    ranked = rank_candidates(
        sample_candidates
    )

    print("Candidate Ranking")
    print("=" * 50)

    for index, candidate in enumerate(
        ranked,
        start=1
    ):

        print(
            f"{get_rank_label(index)} "
            f"{candidate['name']} | "
            f"{candidate['role']} | "
            f"Final Score: "
            f"{candidate['ranking_score']}%"
        )