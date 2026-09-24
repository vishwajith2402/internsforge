# ResumeIQ Test Data

This folder contains sample resumes and job descriptions for testing
the ResumeIQ Resume Screening and Candidate Analysis application.

## Important

These resumes should NOT be added to the training dataset.

They are intended to simulate new resumes submitted by candidates.

## Folder Structure

test_data/
│
├── README_TESTING.md
├── expected_results.csv
│
├── resumes/
│   ├── candidate_001_ml.txt
│   ├── candidate_002_data_scientist.txt
│   ├── candidate_003_data_analyst.txt
│   ├── candidate_004_software_engineer.txt
│   ├── candidate_005_web_developer.txt
│   ├── candidate_006_backend_developer.txt
│   ├── candidate_007_ai_engineer.txt
│   ├── candidate_008_business_analyst.txt
│   ├── candidate_009_cloud_engineer.txt
│   ├── candidate_010_devops_engineer.txt
│   ├── candidate_011_cybersecurity.txt
│   └── candidate_012_database_admin.txt
│
└── job_descriptions/
    ├── machine_learning_engineer.txt
    ├── data_scientist.txt
    ├── data_analyst.txt
    ├── software_engineer.txt
    └── devops_engineer.txt

## How to Test

### 1. Start the application

From the project root:

python app.py

### 2. Individual Resume Test

Open:

resumes/candidate_001_ml.txt

Copy the resume information into the Resume Screening section.

Run the prediction.

Verify:

- Predicted category
- Confidence
- Extracted skills
- Experience
- Education
- Job match score

### 3. Job Matching Test

Open:

job_descriptions/machine_learning_engineer.txt

Copy the job description into the Job Matching section.

Use:

candidate_001_ml.txt

The application should identify matching and missing skills.

### 4. Batch Testing

If Batch Screening is available, process all files inside:

resumes/

The application should process multiple candidates.

### 5. Candidate Ranking

Save multiple candidates and open the ranking/analytics section.

The application should display candidates according to their
calculated scores.

### 6. PDF Report

Select a candidate and generate a PDF report.

Verify that:

- Text is readable
- Candidate information is present
- Prediction is present
- Skills are present
- Matching information is present
- Report is properly formatted

## Important Note

The Expected Category values are reference labels for testing.

The trained machine learning model may produce different predictions
depending on the size, quality and distribution of the training
dataset.

The expected results are therefore not guaranteed predictions.

## Recommended Test Order

1. candidate_001_ml.txt
2. candidate_002_data_scientist.txt
3. candidate_003_data_analyst.txt
4. candidate_004_software_engineer.txt
5. candidate_005_web_developer.txt
6. candidate_006_backend_developer.txt
7. candidate_007_ai_engineer.txt
8. candidate_008_business_analyst.txt
9. candidate_009_cloud_engineer.txt
10. candidate_010_devops_engineer.txt
11. candidate_011_cybersecurity.txt
12. candidate_012_database_admin.txt