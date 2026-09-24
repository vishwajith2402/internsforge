import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "student_data.csv"

REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(
    exist_ok=True
)


COLUMNS = [
    "Student Name",
    "Study Hours",
    "Attendance Percentage",
    "Previous Marks",
    "Final Marks",
    "Result"
]


# ==========================================
# READ CSV
# ==========================================

students = []


with open(
    DATA_FILE,
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:

    reader = csv.reader(file)

    header = next(reader)

    if header != COLUMNS:

        print("ERROR: Incorrect CSV format.")

        raise SystemExit(1)


    for row in reader:

        if len(row) == 6:

            students.append(row)


if len(students) == 0:

    print("No student data found.")

    raise SystemExit(1)


# ==========================================
# DATAFRAME
# ==========================================

df = pd.DataFrame(
    students,
    columns=COLUMNS
)


df["Study Hours"] = pd.to_numeric(
    df["Study Hours"]
)

df["Attendance Percentage"] = pd.to_numeric(
    df["Attendance Percentage"]
)

df["Previous Marks"] = pd.to_numeric(
    df["Previous Marks"]
)

df["Final Marks"] = pd.to_numeric(
    df["Final Marks"]
)


# ==========================================
# AVERAGES
# ==========================================

average_marks = df[
    "Final Marks"
].mean()


average_attendance = df[
    "Attendance Percentage"
].mean()


average_study = df[
    "Study Hours"
].mean()


# ==========================================
# TOP STUDENTS
# ==========================================

top_students = df.nlargest(
    5,
    "Final Marks"
)


low_students = df.nsmallest(
    3,
    "Final Marks"
)


# ==========================================
# PASS / FAIL
# ==========================================

passed = (
    df["Result"]
    .str.lower()
    .eq("pass")
    .sum()
)


failed = (
    df["Result"]
    .str.lower()
    .eq("fail")
    .sum()
)


total = len(df)


pass_percentage = (
    passed / total
) * 100


fail_percentage = (
    failed / total
) * 100


# ==========================================
# CORRELATION
# ==========================================

attendance_correlation = df[
    "Attendance Percentage"
].corr(
    df["Final Marks"]
)


study_correlation = df[
    "Study Hours"
].corr(
    df["Final Marks"]
)


# ==========================================
# PRINT ANALYSIS
# ==========================================

print()
print("==========================================")
print(" STUDENT PERFORMANCE ANALYSIS")
print("==========================================")


print()
print("Total Students:", total)

print(
    "Average Final Marks:",
    round(average_marks, 2)
)

print(
    "Average Attendance:",
    round(average_attendance, 2),
    "%"
)

print(
    "Average Study Hours:",
    round(average_study, 2)
)


print()
print("PASS / FAIL")

print(
    "Passed:",
    passed
)

print(
    "Failed:",
    failed
)

print(
    "Pass Percentage:",
    round(pass_percentage, 2),
    "%"
)

print(
    "Fail Percentage:",
    round(fail_percentage, 2),
    "%"
)


print()
print("TOP 5 STUDENTS")

print(
    top_students[
        [
            "Student Name",
            "Final Marks",
            "Attendance Percentage",
            "Result"
        ]
    ].to_string(
        index=False
    )
)


print()
print("LOW PERFORMING STUDENTS")

print(
    low_students[
        [
            "Student Name",
            "Final Marks",
            "Result"
        ]
    ].to_string(
        index=False
    )
)


print()
print("PERFORMANCE FACTORS")

print(
    "Attendance vs Marks:",
    round(
        attendance_correlation,
        2
    )
)

print(
    "Study Hours vs Marks:",
    round(
        study_correlation,
        2
    )
)


# ==========================================
# REPORT
# ==========================================

report = f"""
STUDENT PERFORMANCE ANALYSIS REPORT
====================================

Total Students: {total}

Average Final Marks: {average_marks:.2f}

Average Attendance: {average_attendance:.2f}%

Average Study Hours: {average_study:.2f}

Passed Students: {passed}

Failed Students: {failed}

Pass Percentage: {pass_percentage:.2f}%

Fail Percentage: {fail_percentage:.2f}%


TOP 5 STUDENTS
--------------

{top_students[
    [
        "Student Name",
        "Final Marks",
        "Attendance Percentage",
        "Result"
    ]
].to_string(index=False)}


LOW PERFORMING STUDENTS
-----------------------

{low_students[
    [
        "Student Name",
        "Final Marks",
        "Result"
    ]
].to_string(index=False)}


PERFORMANCE FACTORS
-------------------

Attendance vs Final Marks:
{attendance_correlation:.2f}

Study Hours vs Final Marks:
{study_correlation:.2f}
"""


with open(

    REPORT_DIR /
    "analysis_report.txt",

    "w",

    encoding="utf-8"

) as file:

    file.write(report)


# ==========================================
# CHART 1
# ==========================================

plt.figure(
    figsize=(10, 5)
)

sns.barplot(
    data=df,
    x="Student Name",
    y="Final Marks"
)

plt.title(
    "Final Marks by Student"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    REPORT_DIR /
    "final_marks.png"
)

plt.close()


# ==========================================
# CHART 2
# ==========================================

plt.figure(
    figsize=(7, 5)
)

sns.scatterplot(
    data=df,

    x="Attendance Percentage",

    y="Final Marks",

    hue="Result",

    s=100
)

plt.title(
    "Attendance vs Final Marks"
)

plt.tight_layout()

plt.savefig(
    REPORT_DIR /
    "attendance_vs_marks.png"
)

plt.close()


# ==========================================
# CHART 3
# ==========================================

plt.figure(
    figsize=(7, 5)
)

sns.scatterplot(
    data=df,

    x="Study Hours",

    y="Final Marks",

    hue="Result",

    s=100
)

plt.title(
    "Study Hours vs Final Marks"
)

plt.tight_layout()

plt.savefig(
    REPORT_DIR /
    "study_hours_vs_marks.png"
)

plt.close()


print()
print("==========================================")
print(" ANALYSIS COMPLETED SUCCESSFULLY")
print("==========================================")

print()
print(
    "Report saved at:"
)

print(
    REPORT_DIR /
    "analysis_report.txt"
)

print()
print(
    "Charts saved at:"
)

print(
    REPORT_DIR
)