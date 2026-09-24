# ResumeIQ — Intelligent Resume Screening & Candidate Analysis

> **An ML and NLP-powered desktop application for automated resume classification, job matching, candidate ranking, skill analysis, and HR-focused recruitment analytics.**

---

## 📌 Project Overview

**ResumeIQ** is a Python-based Machine Learning and Natural Language Processing application designed to help HR teams automate the initial screening and classification of resumes.

Recruiters often receive hundreds or thousands of resumes for a single job opening. Manually reading and categorizing every resume is time-consuming and can lead to inconsistent screening.

ResumeIQ addresses this problem by using:

* Natural Language Processing (NLP)
* TF-IDF text vectorization
* Machine Learning classification
* Resume parsing
* Skill extraction
* Job-description matching
* Candidate ranking
* Candidate database management
* Recruitment analytics
* PDF report generation

The application provides a graphical desktop interface built using **Tkinter**, so Streamlit is not required.

---

# 🎯 Project Objective

The main objective of ResumeIQ is to develop an intelligent resume screening system that can automatically analyze resumes and assist recruiters in identifying suitable candidates.

The system can:

1. Read resume information.
2. Clean and preprocess resume text.
3. Extract relevant skills and information.
4. Convert text into numerical features using TF-IDF.
5. Classify resumes into job categories.
6. Compare resumes with job descriptions.
7. Calculate candidate matching scores.
8. Identify skill matches and skill gaps.
9. Rank candidates.
10. Store candidate information.
11. Generate recruitment reports.
12. Provide analytics through a desktop user interface.

---

# 🧠 Machine Learning Problem

### Problem Statement

HR teams receive a large number of resumes for different job roles. Manually reviewing these resumes is inefficient and time-consuming.

ResumeIQ automatically analyzes resume content and predicts the most suitable job category using Machine Learning and NLP techniques.

### Machine Learning Type

**Supervised Machine Learning + Natural Language Processing**

### Main ML Task

**Text Classification**

Input:

```text
Resume Text
+
Skills
+
Experience
+
Education
```

Output:

```text
Predicted Job Category
+
Prediction Confidence
+
Matching Analysis
```

---

# 🤖 Machine Learning Algorithms

The project supports multiple classification algorithms:

### 1. Naive Bayes

Naive Bayes is a probabilistic classification algorithm commonly used for text classification.

Advantages:

* Fast
* Simple
* Works well with high-dimensional text data
* Suitable for NLP problems

---

### 2. Logistic Regression

Logistic Regression is used for classification and provides a strong baseline for text-based classification problems.

Advantages:

* Efficient
* Interpretable
* Performs well with TF-IDF features
* Suitable for multi-class classification

---

### 3. Support Vector Machine

Support Vector Machine (SVM) is effective for high-dimensional datasets such as TF-IDF text representations.

Advantages:

* Strong text classification performance
* Works well with sparse features
* Effective for multi-class classification

---

### 4. Random Forest

Random Forest is an ensemble learning algorithm based on multiple decision trees.

Advantages:

* Robust
* Handles nonlinear relationships
* Useful for structured resume features
* Provides an additional classification approach

---

# 🔄 How ResumeIQ Works

The complete system follows this workflow:

```text
                 Resume
                   │
                   ▼
          Resume Input / Upload
                   │
                   ▼
          Text Extraction
                   │
                   ▼
          Text Preprocessing
                   │
                   ▼
       Stopword & Special Character
              Removal
                   │
                   ▼
             TF-IDF
            Vectorization
                   │
                   ▼
       Machine Learning Model
                   │
                   ▼
       Job Category Prediction
                   │
          ┌────────┴────────┐
          ▼                 ▼
    Skill Analysis       Job Matching
          │                 │
          └────────┬────────┘
                   ▼
          Candidate Scoring
                   │
                   ▼
          Candidate Ranking
                   │
                   ▼
       Analytics & Reporting
                   │
                   ▼
             HR Decision
```

---

# ⚙️ Working Process

## Step 1 — Resume Input

The user can provide resume information through the ResumeIQ interface.

The system accepts resume content and extracts relevant information such as:

* Resume text
* Skills
* Experience
* Education
* Job-related keywords

---

## Step 2 — Text Cleaning

Raw resume text normally contains:

* Special characters
* Unnecessary spaces
* Punctuation
* Stopwords
* Different text formats
* Uppercase/lowercase variations

The preprocessing module cleans the text.

Example:

### Before

```text
Python, MACHINE Learning!!! Developer with 2+ years
of experience in Data Analysis.
```

### After

```text
python machine learning developer years experience
data analysis
```

---

# 🧹 NLP Preprocessing

The preprocessing pipeline performs operations such as:

### Lowercasing

```text
Python → python
```

### Special Character Removal

```text
Python!!! → Python
```

### Whitespace Normalization

```text
Python     Machine Learning
```

becomes:

```text
Python Machine Learning
```

### Stopword Removal

Common words that provide little classification value can be removed.

Example:

```text
the
is
and
of
with
```

---

# 🔢 TF-IDF Vectorization

Machine Learning algorithms cannot directly understand raw text.

Therefore, ResumeIQ converts text into numerical features using **TF-IDF — Term Frequency-Inverse Document Frequency**.

TF-IDF measures how important a word is within a document compared with the complete dataset.

For example:

```text
Python
Machine Learning
SQL
NLP
TensorFlow
AWS
```

are converted into numerical feature values.

The resulting matrix is then supplied to the Machine Learning model.

---

# 🧠 Model Training

The cleaned dataset is divided into:

```text
Training Dataset
Testing Dataset
```

The training data is used to learn relationships between resume text and job categories.

Example:

```text
Resume Text
     ↓
TF-IDF
     ↓
Machine Learning Model
     ↓
Job Category
```

---

# 🎯 Resume Classification

After training, ResumeIQ can predict the category of a new resume.

Example:

```text
Input Resume

Python
Pandas
NumPy
Scikit-learn
Machine Learning
SQL
Data Analysis
```

Possible prediction:

```text
Predicted Category:
Data Scientist

Confidence:
87%
```

---

# 💼 Job Matching

ResumeIQ can compare a candidate's resume against a job description.

Example:

### Job Requirements

```text
Python
Machine Learning
SQL
NLP
Docker
AWS
```

### Candidate Skills

```text
Python
Machine Learning
SQL
NLP
Pandas
NumPy
```

The system identifies:

### Matched Skills

```text
✓ Python
✓ Machine Learning
✓ SQL
✓ NLP
```

### Missing Skills

```text
✗ Docker
✗ AWS
```

A matching score is then calculated.

Example:

```text
Job Match Score: 82%
```

---

# 📊 Candidate Ranking

Candidates can be ranked according to their overall suitability.

Example:

```text
Candidate             Score
--------------------------------
Candidate A           92%
Candidate B           87%
Candidate C           81%
Candidate D           73%
Candidate E           64%
```

This allows HR teams to focus on the strongest candidates first.

---

# 📈 Candidate Analytics

ResumeIQ provides analytics related to:

* Candidate scores
* Job categories
* Skills
* Experience
* Education
* Resume classifications
* Matching performance

These analytics can help recruiters understand the candidate pool.

---

# 📄 PDF Report Generation

The application can generate a structured PDF report containing candidate information.

A report can include:

```text
Candidate Information
---------------------
Candidate Name
Predicted Job Category
ML Confidence
Job Match Score
Text Similarity
Skill Match
Detected Skills
Skill Gaps
Recommendation
```

The generated report can be used for:

* HR review
* Candidate comparison
* Internship demonstration
* Project presentation
* Documentation

---

# 🖥️ User Interface

ResumeIQ uses **Tkinter** for the desktop graphical interface.

### Why Tkinter?

Tkinter was selected because:

* It is included with standard Python installations.
* It does not require a web server.
* It works offline.
* It is lightweight.
* It supports desktop applications.
* It allows custom UI design.

**Streamlit is NOT used in this project.**

---

# 🧩 Main UI Sections

The application contains multiple sections.

## Dashboard

Provides an overview of the application.

Typical information includes:

```text
Total Candidates
Resumes Screened
Strong Matches
Average Match Score
```

---

## Screen Resume

Used for analyzing an individual resume.

The user can:

1. Enter or upload resume information.
2. Provide a job description.
3. Run resume analysis.
4. View ML prediction.
5. View confidence.
6. View matching score.
7. View detected skills.
8. View skill gaps.
9. Save candidate.
10. Generate a report.

---

## Batch Screening

Used to process multiple resumes.

This is useful when an organization receives many resumes.

Example:

```text
Resume 1 → Data Scientist
Resume 2 → Software Engineer
Resume 3 → Data Analyst
Resume 4 → ML Engineer
```

---

## Candidates

Displays candidates stored by the application.

HR users can review candidate information and ranking information.

---

## Analytics

Displays recruitment-related statistics and insights.

Examples:

* Candidate distribution
* Job category distribution
* Skill frequency
* Match scores
* Candidate performance

---

## System

Provides system and model-related information.

This can be used to verify:

* Model availability
* Dataset status
* Application status
* ML system status

---

# 📁 Project Structure

Recommended project structure:

```text
Resume_Screening_ML/
│
├── app.py
│
├── preprocessing.py
├── train_model.py
├── predict.py
│
├── resume_parser.py
├── skill_extractor.py
├── job_matcher.py
├── candidate_ranker.py
├── candidate_database.py
│
├── report_generator.py
├── analytics.py
├── utils.py
│
├── data/
│   └── resume_dataset.csv
│
├── models/
│   ├── resume_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── output/
│   ├── reports/
│   └── exports/
│
├── requirements.txt
│
└── README.md
```

> The exact files in your project may vary depending on the Phase 3/Phase 4 features enabled.

---

# 📋 Dataset

The primary dataset contains resume-related information.

Expected columns:

```text
Resume Text
Skills
Experience
Education
Job Category
```

Example:

| Resume Text                           | Skills                | Experience | Education  | Job Category         |
| ------------------------------------- | --------------------- | ---------- | ---------- | -------------------- |
| Python developer with ML experience   | Python, ML, SQL       | 2 years    | B.Tech CSE | Machine Learning     |
| Java developer experienced in Spring  | Java, Spring, SQL     | 3 years    | B.Tech IT  | Software Development |
| Data analyst with Power BI experience | Python, SQL, Power BI | 2 years    | B.Sc CS    | Data Analyst         |

---

# 🛠️ Technologies Used

## Programming Language

```text
Python 3.10+
```

## Machine Learning

```text
Scikit-learn
```

## Data Processing

```text
Pandas
NumPy
```

## NLP

```text
NLTK
Scikit-learn TF-IDF
```

## Visualization

Depending on the enabled analytics modules:

```text
Matplotlib
Plotly
```

## GUI

```text
Tkinter
```

## PDF

```text
ReportLab
```

## Database

```text
SQLite
```

## File Processing

Depending on enabled resume parsing features:

```text
PyPDF2 / pypdf
python-docx
```

---

# 📦 Required Libraries

Install the project dependencies using:

```powershell
pip install pandas numpy scikit-learn nltk matplotlib reportlab pypdf python-docx
```

If your project uses Plotly:

```powershell
pip install plotly
```

If your project uses additional file-processing functionality:

```powershell
pip install openpyxl
```

---

# 🐍 Python Version

Recommended:

```text
Python 3.10
Python 3.11
Python 3.12
```

Python versions newer than this may work depending on the installed library versions, but for ML internship projects, **Python 3.10–3.12 is generally recommended for compatibility**.

---

# 🚀 Installation Guide

## Step 1 — Clone or Copy the Project

Place the project in your desired directory.

Example:

```text
D:\Extra\Internsforge\Resume_Screening\Resume_Screening_ML
```

Open this folder in VS Code.

---

# Step 2 — Open Terminal

In VS Code:

```text
Terminal → New Terminal
```

Navigate to the project directory.

```powershell
cd D:\Extra\Internsforge\Resume_Screening\Resume_Screening_ML
```

---

# Step 3 — Create Virtual Environment

Recommended command:

```powershell
python -m venv .venv
```

If Python's `venv` creation fails on your system, make sure Python is correctly installed and that the Python installation includes the required `venv`/pip components.

---

# Step 4 — Activate Virtual Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should show something similar to:

```text
(.venv) PS D:\Extra\Internsforge\Resume_Screening\Resume_Screening_ML>
```

---

# Step 5 — Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

# Step 6 — Install Dependencies

If `requirements.txt` exists:

```powershell
pip install -r requirements.txt
```

Otherwise:

```powershell
pip install pandas numpy scikit-learn nltk matplotlib reportlab pypdf python-docx openpyxl plotly
```

---

# Step 7 — Verify Python

```powershell
python --version
```

Then:

```powershell
python -m pip --version
```

---

# Step 8 — Verify Dataset

Make sure the dataset exists at:

```text
data/resume_dataset.csv
```

Check using PowerShell:

```powershell
Test-Path .\data\resume_dataset.csv
```

Expected:

```text
True
```

You can also check the folder:

```powershell
Get-ChildItem .\data
```

---

# 🧪 Test Dataset

Before training, verify that the CSV contains:

```text
Resume Text
Skills
Experience
Education
Job Category
```

Check using:

```powershell
python -c "import pandas as pd; df=pd.read_csv('data/resume_dataset.csv'); print(df.head()); print(df.columns.tolist())"
```

---

# 🧹 Test Preprocessing

Run:

```powershell
python preprocessing.py
```

If the preprocessing module contains only functions and does not print anything, this command may complete without visible output.

To explicitly test it:

```powershell
python -c "from preprocessing import load_data, prepare_text; df=load_data('data/resume_dataset.csv'); X,y=prepare_text(df); print('PREPROCESSING OK'); print('Documents:',len(X)); print('Categories:',y.unique().tolist())"
```

Expected output should contain:

```text
PREPROCESSING OK
Documents: ...
Categories: [...]
```

---

# 🧠 Train the Machine Learning Model

Run:

```powershell
python train_model.py
```

The training process should:

1. Load the dataset.
2. Clean the resume text.
3. Split the data.
4. Apply TF-IDF.
5. Train the classification model.
6. Evaluate the model.
7. Save the trained model.
8. Save the vectorizer.

The model files should be created in the `models` folder.

Example:

```text
models/
├── resume_model.pkl
└── tfidf_vectorizer.pkl
```

---

# 🔍 Test Prediction

After training:

```powershell
python predict.py
```

Or use a direct test:

```powershell
python -c "from predict import predict_resume; print(predict_resume('Python machine learning pandas numpy scikit learn predictive modeling data analysis','Python Machine Learning Pandas SQL','2 years','B.Tech Computer Science'))"
```

---

# ▶️ Run the Application

Once the model is successfully trained:

```powershell
python app.py
```

The ResumeIQ desktop interface should open.

---

# 🔄 Complete Run Sequence

For a fresh setup, the recommended sequence is:

```powershell
cd D:\Extra\Internsforge\Resume_Screening\Resume_Screening_ML
```

Activate environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Check dataset:

```powershell
Test-Path .\data\resume_dataset.csv
```

Train model:

```powershell
python train_model.py
```

Run application:

```powershell
python app.py
```

---

# 📊 Model Evaluation

The project evaluates the classification model using:

## Accuracy

Measures the percentage of correctly classified resumes.

```text
Accuracy =
Correct Predictions / Total Predictions
```

---

## Precision

Measures how many predicted candidates in a class actually belong to that class.

High precision means fewer false positives.

---

## Recall

Measures how many actual candidates belonging to a category were successfully identified.

High recall means fewer false negatives.

---

## F1 Score

F1 Score combines precision and recall.

```text
F1 = 2 × (Precision × Recall) /
     (Precision + Recall)
```

It is especially useful when the dataset has imbalanced categories.

---

## Confusion Matrix

The confusion matrix shows how predictions are distributed across job categories.

Example:

```text
                 Predicted
              DS   DA   SE
Actual DS     45    3    2
       DA      4   39    5
       SE      2    4   43
```

This helps identify which job categories are being confused by the model.

---

# 📈 Example Workflow

Suppose HR wants to screen a candidate for a Machine Learning Engineer position.

### Candidate Resume

```text
Python developer with experience in machine learning,
deep learning, Pandas, NumPy, Scikit-learn and SQL.
Worked on predictive modeling and NLP projects.
```

### Job Description

```text
Looking for a Machine Learning Engineer with experience
in Python, machine learning, SQL, NLP and cloud technologies.
```

ResumeIQ performs:

```text
Resume
  ↓
Text Cleaning
  ↓
Skill Extraction
  ↓
TF-IDF
  ↓
ML Classification
  ↓
Job Category Prediction
  ↓
Job Description Matching
  ↓
Skill Analysis
  ↓
Candidate Score
  ↓
Recommendation
```

Example:

```text
Predicted Role:
Machine Learning Engineer

ML Confidence:
89%

Job Match:
86%

Matched Skills:
Python
Machine Learning
SQL
NLP

Skill Gaps:
AWS
Docker
```

---

# 🔐 Data Privacy

Resume data can contain personal information.

For production use:

* Do not upload resumes to untrusted services.
* Store candidate data securely.
* Restrict access to candidate records.
* Avoid exposing personally identifiable information.
* Encrypt sensitive data when deploying the system.
* Follow applicable data-protection and employment regulations.

The current project is primarily intended as an educational, internship, and prototype system.

---

# ⚠️ Limitations

ResumeIQ is an ML-assisted screening tool and should not be treated as an autonomous hiring system.

Potential limitations include:

* Model performance depends on dataset quality.
* Small datasets may produce unreliable predictions.
* Biased training data can produce biased predictions.
* Different resume formats may affect text extraction.
* Similar job categories can be difficult to distinguish.
* Keyword-heavy resumes may receive higher scores even when actual ability differs.
* ML confidence is not equivalent to candidate quality.
* Human review remains necessary.

The system should support recruiters rather than make final hiring decisions automatically.

---

# 🧪 Testing

Recommended tests:

### Dataset Test

```powershell
python -c "import pandas as pd; df=pd.read_csv('data/resume_dataset.csv'); print(df.shape); print(df.columns.tolist())"
```

### Preprocessing Test

```powershell
python preprocessing.py
```

### Model Training Test

```powershell
python train_model.py
```

### Prediction Test

```powershell
python predict.py
```

### Application Test

```powershell
python app.py
```

### Syntax Check

```powershell
python -m py_compile app.py
```

---

# 🛠️ Common Problems and Solutions

## Problem: Dataset Not Found

Error:

```text
FileNotFoundError
```

Check:

```powershell
Test-Path .\data\resume_dataset.csv
```

If the result is:

```text
False
```

place the dataset inside:

```text
data/
```

---

## Problem: Empty CSV

Error:

```text
pandas.errors.EmptyDataError:
No columns to parse from file
```

Solution:

Check that:

```text
data/resume_dataset.csv
```

is not empty and contains the correct CSV headers.

---

## Problem: Function Import Error

Example:

```text
ImportError:
cannot import name 'load_data'
```

Make sure the function is actually defined in:

```text
preprocessing.py
```

Likewise, prediction functions should exist in:

```text
predict.py
```

---

## Problem: Model Does Not Exist

Error:

```text
Trained model does not exist.
Run: python train_model.py
```

Solution:

```powershell
python train_model.py
```

before:

```powershell
python app.py
```

---

## Problem: Missing Library

Example:

```text
ModuleNotFoundError:
No module named 'pandas'
```

Install:

```powershell
pip install pandas
```

or install everything:

```powershell
pip install -r requirements.txt
```

---

## Problem: Application Does Not Open

First run:

```powershell
python -m py_compile app.py
```

If there is no output, run:

```powershell
python app.py
```

---

# 🏗️ Project Architecture

```text
                    ┌─────────────────┐
                    │     Resume      │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Resume Processing  │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │    NLP Cleaning     │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │   TF-IDF Features   │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │  ML Classification │
                  └─────────┬───────────┘
                            │
                 ┌──────────┴───────────┐
                 ▼                      ▼
        ┌─────────────────┐    ┌─────────────────┐
        │ Job Prediction  │    │ Skill Analysis  │
        └────────┬────────┘    └────────┬────────┘
                 │                      │
                 └──────────┬───────────┘
                            ▼
                  ┌─────────────────────┐
                  │   Job Matching      │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Candidate Ranking   │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Analytics & Reports │
                  └─────────┬───────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │    HR Dashboard     │
                  └─────────────────────┘
```

---

# 🚀 Future Enhancements

Future versions of ResumeIQ can include:

### Phase 4

* Candidate ranking
* Explainable AI
* Advanced job matching
* Candidate comparison
* Skill demand analytics
* Smart shortlisting
* Recruitment dashboards
* Advanced export functionality

### Future Research Features

* BERT-based resume classification
* Transformer models
* Sentence embeddings
* Semantic similarity
* Large Language Model integration
* Retrieval-Augmented Generation
* Automated interview question generation
* Resume improvement suggestions
* ATS compatibility scoring
* Multilingual resume processing
* Advanced bias detection
* Cloud deployment
* REST API
* Secure multi-user HR platform

---

# 📚 Skills Demonstrated

This project demonstrates practical knowledge of:

### Python

* Functions
* Modules
* File handling
* Object-oriented programming
* Exception handling
* Virtual environments

### Machine Learning

* Supervised learning
* Classification
* Train/test splitting
* Model evaluation
* Model serialization

### NLP

* Text preprocessing
* Stopword removal
* TF-IDF
* Text classification
* Skill extraction

### Data Science

* Pandas
* NumPy
* Data preprocessing
* Data analysis
* Visualization

### Software Development

* Modular architecture
* GUI development
* Database integration
* Report generation
* Error handling
* Testing

### HR Analytics

* Candidate screening
* Job matching
* Candidate ranking
* Skill gap analysis
* Recruitment analytics

---

# 🎓 Internship Learning Outcomes

By completing this project, the following concepts are demonstrated:

```text
Python Programming
        ↓
Data Processing
        ↓
Natural Language Processing
        ↓
TF-IDF
        ↓
Machine Learning
        ↓
Classification
        ↓
Model Evaluation
        ↓
GUI Development
        ↓
Database Management
        ↓
HR Analytics
        ↓
Report Generation
```

---

# 💡 Why This Project Is Useful

Traditional resume screening requires recruiters to manually inspect large numbers of resumes.

ResumeIQ attempts to reduce the initial screening workload by providing automated analysis.

Instead of:

```text
100 Resumes
     ↓
Manual Reading
     ↓
Manual Categorization
     ↓
Manual Comparison
```

ResumeIQ provides:

```text
100 Resumes
     ↓
Automated Processing
     ↓
ML Classification
     ↓
Skill Analysis
     ↓
Job Matching
     ↓
Candidate Ranking
     ↓
Recruiter Review
```

The recruiter remains responsible for the final decision.

---

# 📌 Project Status

```text
Project: ResumeIQ
Type: Machine Learning + NLP
Application: Desktop GUI
Language: Python
UI Framework: Tkinter
ML: Scikit-learn
NLP: TF-IDF
Database: SQLite
Reports: PDF
Status: Active Development
```

---

# 👨‍💻 Author

**Vishwajith**

Machine Learning & Python Project

Developed as part of an internship/project-based learning program.

---

# ⭐ Acknowledgement

This project was developed for educational and internship purposes to demonstrate the practical application of:

* Machine Learning
* Natural Language Processing
* Python
* Data Science
* HR Analytics
* Desktop Application Development

---

# 📜 Disclaimer

ResumeIQ is an educational/prototype recruitment assistance system.

The predictions, scores, rankings, and recommendations generated by the application should not be used as the sole basis for employment decisions.

Final recruitment decisions should always involve qualified human review.

---

# ⭐ If You Like This Project

If this project is useful, consider:

* Giving the project a star on GitHub
* Forking the project
* Improving the ML model
* Adding new resume categories
* Contributing new NLP features
* Improving the UI
* Adding additional analytics
* Experimenting with transformer-based NLP models
