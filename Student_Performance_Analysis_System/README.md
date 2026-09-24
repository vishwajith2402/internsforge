# Student Performance Analysis System

## Project Objective

To analyze student marks, attendance, and study hours using Python and generate useful insights.

## Features

* Load student data from CSV
* Display student data
* Calculate average marks
* Find top-performing students
* Find low-performing students
* Compare attendance with marks
* Compare study hours with marks
* Generate charts
* Generate an analysis report

## Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Tkinter

## Folder Structure

```text
Student_Performance_Analysis_System/
│
├── data/
│   └── student_data.csv
│
├── reports/
│
├── src/
│   ├── app.py
│   └── analysis.py
│
├── requirements.txt
└── README.md
```

## Installation

Open PowerShell inside the project folder.

Install the required libraries:

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

Run:

```powershell
python src\app.py
```

The GUI will open.

## Run Analysis

Click:

```text
Run Analysis
```

The following files will be generated inside the `reports` folder:

```text
analysis_report.txt
final_marks.png
attendance_vs_marks.png
study_hours_vs_marks.png
```

## Run Without GUI

You can also run the analysis directly:

```powershell
python src\analysis.py
```

## Dataset

The dataset is located at:

```text
data\student_data.csv
```

The required columns are:

```text
Student Name
Study Hours
Attendance Percentage
Previous Marks
Final Marks
Result
```

## Example Dataset

```csv
Student Name,Study Hours,Attendance Percentage,Previous Marks,Final Marks,Result
Vishwa,8,90,85,88,Pass
Rahul,4,65,60,55,Fail
Anu,7,85,78,82,Pass
```

## Project Workflow

```text
Student CSV
     ↓
Load Data
     ↓
Data Analysis
     ↓
Average Marks
     ↓
Top & Low Students
     ↓
Attendance Analysis
     ↓
Study Hours Analysis
     ↓
Charts
     ↓
Report
```

## Skills Learned

* Python programming
* CSV file handling
* Pandas
* NumPy
* Data cleaning
* Data analysis
* Data visualization
* Matplotlib
* Seaborn
* Basic GUI development
* Basic reporting

## Troubleshooting

### Pandas error

```powershell
python -m pip install pandas
```

### NumPy error

```powershell
python -m pip install numpy
```

### Matplotlib error

```powershell
python -m pip install matplotlib
```

### Seaborn error

```powershell
python -m pip install seaborn
```

### Check Python

```powershell
python --version
```

### Check Tkinter

```powershell
python -m tkinter
```

## Final Run Command

From the project folder:

```powershell
python -m pip install -r requirements.txt
python src\app.py
```
