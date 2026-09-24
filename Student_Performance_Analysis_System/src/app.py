import tkinter as tk
from tkinter import ttk, messagebox
import csv
import subprocess
import sys
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "student_data.csv"

ANALYSIS_FILE = BASE_DIR / "src" / "analysis.py"


# ==========================================
# CSV COLUMNS
# ==========================================

COLUMNS = [
    "Student Name",
    "Study Hours",
    "Attendance Percentage",
    "Previous Marks",
    "Final Marks",
    "Result"
]


# ==========================================
# READ DATA
# ==========================================

def read_data():

    students = []

    try:

        with open(
            DATA_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.reader(file)

            header = next(reader, None)

            if header != COLUMNS:
                raise ValueError("CSV columns are incorrect.")

            for row in reader:

                if len(row) == 6:
                    students.append(row)

        return students

    except Exception as error:

        messagebox.showerror(
            "Dataset Error",
            str(error)
        )

        return []


# ==========================================
# SAVE DATA
# ==========================================

def save_data(students):

    try:

        with open(
            DATA_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(COLUMNS)

            writer.writerows(students)

        return True

    except Exception as error:

        messagebox.showerror(
            "Save Error",
            str(error)
        )

        return False


# ==========================================
# CALCULATE RESULT
# ==========================================

def calculate_result(final_marks):

    if final_marks >= 50:
        return "Pass"

    return "Fail"


# ==========================================
# UPDATE DASHBOARD
# ==========================================

def update_dashboard(students):

    total = len(students)

    if total == 0:

        total_value.config(text="0")
        average_value.config(text="0")
        pass_value.config(text="0%")
        attendance_value.config(text="0%")

        return


    marks = [
        float(student[4])
        for student in students
    ]

    attendance = [
        float(student[2])
        for student in students
    ]


    passed = sum(
        1
        for student in students
        if student[5].lower() == "pass"
    )


    average_marks = sum(marks) / total

    average_attendance = (
        sum(attendance) / total
    )

    pass_percentage = (
        passed / total
    ) * 100


    total_value.config(
        text=str(total)
    )

    average_value.config(
        text=f"{average_marks:.2f}"
    )

    pass_value.config(
        text=f"{pass_percentage:.2f}%"
    )

    attendance_value.config(
        text=f"{average_attendance:.2f}%"
    )


# ==========================================
# REFRESH TABLE
# ==========================================

def refresh_table():

    students = read_data()


    # Clear table

    for item in tree.get_children():

        tree.delete(item)


    # Add data

    for student in students:

        tree.insert(
            "",
            "end",
            values=student
        )


    update_dashboard(students)


# ==========================================
# CLEAR INPUTS
# ==========================================

def clear_inputs():

    name_entry.delete(
        0,
        tk.END
    )

    study_entry.delete(
        0,
        tk.END
    )

    attendance_entry.delete(
        0,
        tk.END
    )

    previous_entry.delete(
        0,
        tk.END
    )

    final_entry.delete(
        0,
        tk.END
    )

    name_entry.focus()


# ==========================================
# VALIDATE STUDENT DATA
# ==========================================

def get_student_values():

    name = name_entry.get().strip()

    study = study_entry.get().strip()

    attendance = attendance_entry.get().strip()

    previous = previous_entry.get().strip()

    final = final_entry.get().strip()


    if (
        name == ""
        or study == ""
        or attendance == ""
        or previous == ""
        or final == ""
    ):

        messagebox.showwarning(
            "Missing Data",
            "Please enter all student details."
        )

        return None


    try:

        study_value = float(study)

        attendance_value = float(attendance)

        previous_value = float(previous)

        final_value = float(final)

    except ValueError:

        messagebox.showerror(
            "Invalid Data",
            "Please enter numbers only."
        )

        return None


    if study_value < 0:

        messagebox.showerror(
            "Invalid Data",
            "Study hours cannot be negative."
        )

        return None


    if attendance_value < 0 or attendance_value > 100:

        messagebox.showerror(
            "Invalid Data",
            "Attendance must be between 0 and 100."
        )

        return None


    if previous_value < 0 or previous_value > 100:

        messagebox.showerror(
            "Invalid Data",
            "Previous marks must be between 0 and 100."
        )

        return None


    if final_value < 0 or final_value > 100:

        messagebox.showerror(
            "Invalid Data",
            "Final marks must be between 0 and 100."
        )

        return None


    result = calculate_result(
        final_value
    )


    return [
        name,
        study_value,
        attendance_value,
        previous_value,
        final_value,
        result
    ]


# ==========================================
# ADD STUDENT
# ==========================================

def add_student():

    new_student = get_student_values()


    if new_student is None:
        return


    students = read_data()


    # Check duplicate name

    for student in students:

        if student[0].lower() == new_student[0].lower():

            messagebox.showwarning(
                "Duplicate Student",
                "A student with this name already exists."
            )

            return


    students.append(
        new_student
    )


    if save_data(students):

        messagebox.showinfo(
            "Success",
            f"{new_student[0]} added successfully!\n\n"
            f"Result: {new_student[5]}"
        )

        clear_inputs()

        refresh_table()


# ==========================================
# GET SELECTED STUDENT
# ==========================================

def get_selected_student():

    selected = tree.selection()


    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select a student from the table."
        )

        return None


    item = tree.item(
        selected[0]
    )


    return selected[0], list(item["values"])


# ==========================================
# EDIT STUDENT
# ==========================================

def edit_student():

    selected_data = get_selected_student()


    if selected_data is None:
        return


    item_id, student = selected_data


    # Fill input boxes

    clear_inputs()


    name_entry.insert(
        0,
        student[0]
    )

    study_entry.insert(
        0,
        student[1]
    )

    attendance_entry.insert(
        0,
        student[2]
    )

    previous_entry.insert(
        0,
        student[3]
    )

    final_entry.insert(
        0,
        student[4]
    )


    edit_mode["active"] = True

    edit_mode["old_name"] = student[0]

    edit_mode["item_id"] = item_id


    add_button.config(
        text="Update Student",
        command=update_student
    )


    cancel_button.pack(
        side="left",
        padx=5
    )


# ==========================================
# UPDATE STUDENT
# ==========================================

def update_student():

    new_student = get_student_values()


    if new_student is None:
        return


    students = read_data()


    old_name = edit_mode["old_name"]


    # Check duplicate name

    for student in students:

        if (
            student[0].lower()
            == new_student[0].lower()
            and student[0].lower()
            != old_name.lower()
        ):

            messagebox.showwarning(
                "Duplicate Student",
                "Another student with this name already exists."
            )

            return


    # Find old student

    found = False


    for index, student in enumerate(students):

        if student[0] == old_name:

            students[index] = new_student

            found = True

            break


    if not found:

        messagebox.showerror(
            "Error",
            "Student could not be found."
        )

        reset_edit_mode()

        return


    if save_data(students):

        messagebox.showinfo(
            "Updated",
            f"{new_student[0]} updated successfully!"
        )

        reset_edit_mode()

        refresh_table()


# ==========================================
# RESET EDIT MODE
# ==========================================

def reset_edit_mode():

    edit_mode["active"] = False

    edit_mode["old_name"] = ""

    edit_mode["item_id"] = ""


    add_button.config(
        text="Add Student",
        command=add_student
    )


    cancel_button.pack_forget()


    clear_inputs()


# ==========================================
# DELETE STUDENT
# ==========================================

def delete_student():

    selected_data = get_selected_student()


    if selected_data is None:
        return


    item_id, student = selected_data


    name = student[0]


    answer = messagebox.askyesno(

        "Delete Student",

        f"Are you sure you want to delete {name}?"
    )


    if not answer:
        return


    students = read_data()


    new_students = [

        student_data
        for student_data in students
        if student_data[0] != name
    ]


    if save_data(new_students):

        messagebox.showinfo(
            "Deleted",
            f"{name} deleted successfully."
        )

        reset_edit_mode()

        refresh_table()


# ==========================================
# SEARCH STUDENT
# ==========================================

def search_student():

    search_text = search_entry.get().strip().lower()


    if search_text == "":

        refresh_table()

        return


    students = read_data()


    for item in tree.get_children():

        tree.delete(item)


    found = False


    for student in students:

        if search_text in student[0].lower():

            tree.insert(
                "",
                "end",
                values=student
            )

            found = True


    if not found:

        messagebox.showinfo(
            "Search",
            "No student found."
        )


# ==========================================
# SHOW ALL STUDENTS
# ==========================================

def show_all_students():

    search_entry.delete(
        0,
        tk.END
    )

    refresh_table()


# ==========================================
# STUDENT DETAILS
# ==========================================

def student_details():

    selected_data = get_selected_student()


    if selected_data is None:
        return


    item_id, student = selected_data


    name = student[0]

    study = float(student[1])

    attendance = float(student[2])

    previous = float(student[3])

    final = float(student[4])

    result = student[5]


    improvement = final - previous


    # New window

    window = tk.Toplevel(root)

    window.title(
        "Student Details"
    )

    window.geometry(
        "500x600"
    )

    window.resizable(
        False,
        False
    )


    tk.Label(

        window,

        text="Student Details",

        font=(
            "Arial",
            22,
            "bold"
        )

    ).pack(
        pady=20
    )


    tk.Label(

        window,

        text=name,

        font=(
            "Arial",
            18,
            "bold"
        )

    ).pack(
        pady=5
    )


    details_frame = tk.LabelFrame(

        window,

        text="Performance Information",

        font=(
            "Arial",
            12,
            "bold"
        ),

        padx=20,

        pady=15
    )

    details_frame.pack(

        fill="x",

        padx=30,

        pady=15
    )


    details = [

        ("Study Hours", f"{study} hours"),

        ("Attendance", f"{attendance}%"),

        ("Previous Marks", f"{previous}/100"),

        ("Final Marks", f"{final}/100"),

        ("Result", result),

        (
            "Mark Improvement",
            f"{improvement:+.2f}"
        )
    ]


    for label, value in details:

        row = tk.Frame(
            details_frame
        )

        row.pack(
            fill="x",
            pady=7
        )


        tk.Label(

            row,

            text=label,

            font=(
                "Arial",
                11,
                "bold"
            ),

            width=20,

            anchor="w"

        ).pack(
            side="left"
        )


        tk.Label(

            row,

            text=value,

            font=(
                "Arial",
                11
            ),

            anchor="w"

        ).pack(
            side="left"
        )


    # Performance analysis

    analysis_frame = tk.LabelFrame(

        window,

        text="Performance Analysis",

        font=(
            "Arial",
            12,
            "bold"
        ),

        padx=15,

        pady=15
    )

    analysis_frame.pack(

        fill="x",

        padx=30,

        pady=10
    )


    messages = []


    if attendance >= 75:

        messages.append(
            "• Good attendance"
        )

    else:

        messages.append(
            "• Attendance needs improvement"
        )


    if study >= 4:

        messages.append(
            "• Study hours are good"
        )

    else:

        messages.append(
            "• Increase study hours"
        )


    if final >= 75:

        messages.append(
            "• Strong academic performance"
        )

    elif final >= 50:

        messages.append(
            "• Satisfactory academic performance"
        )

    else:

        messages.append(
            "• Academic performance needs attention"
        )


    if improvement > 0:

        messages.append(
            "• Marks improved from previous exam"
        )

    elif improvement < 0:

        messages.append(
            "• Marks decreased from previous exam"
        )

    else:

        messages.append(
            "• Marks remained the same"
        )


    for message in messages:

        tk.Label(

            analysis_frame,

            text=message,

            font=(
                "Arial",
                10
            ),

            anchor="w"

        ).pack(

            fill="x",

            pady=3
        )


    tk.Button(

        window,

        text="Close",

        width=20,

        command=window.destroy

    ).pack(
        pady=20
    )


# ==========================================
# STUDENTS NEEDING ATTENTION
# ==========================================

def students_needing_attention():

    students = read_data()


    if len(students) == 0:

        messagebox.showwarning(
            "No Data",
            "No student data available."
        )

        return


    attention_students = []


    for student in students:

        name = student[0]

        study = float(student[1])

        attendance = float(student[2])

        final = float(student[4])


        reasons = []


        if final < 50:

            reasons.append(
                "Low marks"
            )


        if attendance < 75:

            reasons.append(
                "Low attendance"
            )


        if study < 4:

            reasons.append(
                "Low study hours"
            )


        if len(reasons) > 0:

            attention_students.append(

                (
                    name,
                    study,
                    attendance,
                    final,
                    ", ".join(reasons)
                )
            )


    # Window

    window = tk.Toplevel(root)

    window.title(
        "Students Needing Attention"
    )

    window.geometry(
        "900x550"
    )


    tk.Label(

        window,

        text="Students Needing Attention",

        font=(
            "Arial",
            22,
            "bold"
        )

    ).pack(
        pady=20
    )


    tk.Label(

        window,

        text=
        "Students with low marks, attendance, or study hours",

        font=(
            "Arial",
            10
        )

    ).pack(
        pady=5
    )


    if len(attention_students) == 0:

        tk.Label(

            window,

            text=
            "No students currently need attention.",

            font=(
                "Arial",
                14,
                "bold"
            )

        ).pack(
            pady=50
        )

        return


    attention_tree = ttk.Treeview(

        window,

        columns=(

            "Name",
            "Study",
            "Attendance",
            "Marks",
            "Reason"

        ),

        show="headings",

        height=15
    )


    headings = {

        "Name": "Student Name",

        "Study": "Study Hours",

        "Attendance": "Attendance %",

        "Marks": "Final Marks",

        "Reason": "Reason"
    }


    widths = {

        "Name": 160,

        "Study": 120,

        "Attendance": 140,

        "Marks": 120,

        "Reason": 300
    }


    for column in headings:

        attention_tree.heading(

            column,

            text=headings[column]
        )

        attention_tree.column(

            column,

            width=widths[column],

            anchor="center"
        )


    for student in attention_students:

        attention_tree.insert(

            "",

            "end",

            values=student
        )


    attention_tree.pack(

        fill="both",

        expand=True,

        padx=25,

        pady=15
    )


    tk.Button(

        window,

        text="Close",

        width=20,

        command=window.destroy

    ).pack(
        pady=15
    )


# ==========================================
# OVERALL ANALYSIS
# ==========================================

def overall_analysis():

    students = read_data()


    if len(students) == 0:

        messagebox.showwarning(
            "No Data",
            "No student data available."
        )

        return


    try:

        result = subprocess.run(

            [
                sys.executable,
                str(ANALYSIS_FILE)
            ],

            cwd=str(BASE_DIR),

            capture_output=True,

            text=True
        )


        if result.returncode == 0:

            messagebox.showinfo(

                "Analysis Completed",

                "Overall analysis completed successfully!\n\n"
                "Check the reports folder."
            )

        else:

            messagebox.showerror(

                "Analysis Error",

                result.stderr
            )

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )


# ==========================================
# TOP STUDENT ANALYSIS
# ==========================================

def top_student_analysis():

    students = read_data()


    if len(students) == 0:

        messagebox.showwarning(
            "No Data",
            "No student data available."
        )

        return


    top_marks = max(

        students,

        key=lambda x: float(x[4])
    )


    top_attendance = max(

        students,

        key=lambda x: float(x[2])
    )


    top_study = max(

        students,

        key=lambda x: float(x[1])
    )


    total = len(students)


    passed = sum(

        1
        for student in students
        if student[5].lower() == "pass"
    )


    failed = total - passed


    pass_percentage = (
        passed / total
    ) * 100


    fail_percentage = (
        failed / total
    ) * 100


    sorted_students = sorted(

        students,

        key=lambda x: float(x[4]),

        reverse=True
    )


    window = tk.Toplevel(root)

    window.title(
        "Top Student Analysis"
    )

    window.geometry(
        "850x700"
    )

    window.minsize(
        750,
        600
    )


    tk.Label(

        window,

        text="Top Student Analysis",

        font=(
            "Arial",
            22,
            "bold"
        )

    ).pack(
        pady=20
    )


    # Highest marks

    marks_frame = tk.LabelFrame(

        window,

        text="Highest Final Marks",

        font=(
            "Arial",
            12,
            "bold"
        ),

        padx=20,

        pady=15
    )

    marks_frame.pack(

        fill="x",

        padx=30,

        pady=8
    )


    tk.Label(

        marks_frame,

        text=top_marks[0],

        font=(
            "Arial",
            17,
            "bold"
        )

    ).pack()


    tk.Label(

        marks_frame,

        text=f"Final Marks: {top_marks[4]} / 100"

    ).pack(
        pady=5
    )


    # Highest attendance

    attendance_frame = tk.LabelFrame(

        window,

        text="Highest Attendance",

        font=(
            "Arial",
            12,
            "bold"
        ),

        padx=20,

        pady=15
    )

    attendance_frame.pack(

        fill="x",

        padx=30,

        pady=8
    )


    tk.Label(

        attendance_frame,

        text=top_attendance[0],

        font=(
            "Arial",
            15,
            "bold"
        )

    ).pack()


    tk.Label(

        attendance_frame,

        text=f"Attendance: {top_attendance[2]}%"

    ).pack(
        pady=5
    )


    # Highest study hours

    study_frame = tk.LabelFrame(

        window,

        text="Highest Study Hours",

        font=(
            "Arial",
            12,
            "bold"
        ),

        padx=20,

        pady=15
    )

    study_frame.pack(

        fill="x",

        padx=30,

        pady=8
    )


    tk.Label(

        study_frame,

        text=top_study[0],

        font=(
            "Arial",
            15,
            "bold"
        )

    ).pack()


    tk.Label(

        study_frame,

        text=f"Study Hours: {top_study[1]}"

    ).pack(
        pady=5
    )


    # Pass percentage

    result_frame = tk.LabelFrame(

        window,

        text="Class Result",

        font=(
            "Arial",
            12,
            "bold"
        ),

        padx=20,

        pady=10
    )

    result_frame.pack(

        fill="x",

        padx=30,

        pady=8
    )


    tk.Label(

        result_frame,

        text=
        f"Pass Percentage: {pass_percentage:.2f}%",

        font=(
            "Arial",
            11,
            "bold"
        )

    ).pack(
        pady=3
    )


    tk.Label(

        result_frame,

        text=
        f"Fail Percentage: {fail_percentage:.2f}%"

    ).pack(
        pady=3
    )


    # Top 5

    tk.Label(

        window,

        text="Top 5 Students by Final Marks",

        font=(
            "Arial",
            13,
            "bold"
        )

    ).pack(
        pady=10
    )


    top_tree = ttk.Treeview(

        window,

        columns=(

            "Rank",
            "Name",
            "Marks",
            "Attendance",
            "Result"

        ),

        show="headings",

        height=5
    )


    headings = {

        "Rank": "Rank",

        "Name": "Student Name",

        "Marks": "Final Marks",

        "Attendance": "Attendance %",

        "Result": "Result"
    }


    for column in headings:

        top_tree.heading(

            column,

            text=headings[column]
        )

        top_tree.column(

            column,

            width=140,

            anchor="center"
        )


    for rank, student in enumerate(

        sorted_students[:5],

        start=1

    ):

        top_tree.insert(

            "",

            "end",

            values=(

                rank,

                student[0],

                student[4],

                student[2],

                student[5]

            )
        )


    top_tree.pack(

        fill="x",

        padx=30,

        pady=5
    )


    tk.Button(

        window,

        text="Close",

        width=20,

        command=window.destroy

    ).pack(
        pady=20
    )


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Student Performance Analysis System"
)

root.geometry(
    "1250x800"
)

root.minsize(
    1050,
    700
)


# ==========================================
# EDIT MODE
# ==========================================

edit_mode = {

    "active": False,

    "old_name": "",

    "item_id": ""
}


# ==========================================
# TITLE
# ==========================================

tk.Label(

    root,

    text="Student Performance Analysis System",

    font=(
        "Arial",
        23,
        "bold"
    )

).pack(
    pady=15
)


tk.Label(

    root,

    text=
    "Manage student data and analyze academic performance",

    font=(
        "Arial",
        11
    )

).pack()


# ==========================================
# DASHBOARD
# ==========================================

dashboard_frame = tk.Frame(root)

dashboard_frame.pack(

    fill="x",

    padx=20,

    pady=15
)


# Total students

card1 = tk.LabelFrame(

    dashboard_frame,

    text="Total Students",

    font=(
        "Arial",
        10,
        "bold"
    ),

    padx=30,

    pady=10
)

card1.pack(

    side="left",

    expand=True,

    fill="x",

    padx=5
)


total_value = tk.Label(

    card1,

    text="0",

    font=(
        "Arial",
        20,
        "bold"
    )
)

total_value.pack()


# Average marks

card2 = tk.LabelFrame(

    dashboard_frame,

    text="Average Marks",

    font=(
        "Arial",
        10,
        "bold"
    ),

    padx=30,

    pady=10
)

card2.pack(

    side="left",

    expand=True,

    fill="x",

    padx=5
)


average_value = tk.Label(

    card2,

    text="0",

    font=(
        "Arial",
        20,
        "bold"
    )
)

average_value.pack()


# Pass percentage

card3 = tk.LabelFrame(

    dashboard_frame,

    text="Pass Percentage",

    font=(
        "Arial",
        10,
        "bold"
    ),

    padx=30,

    pady=10
)

card3.pack(

    side="left",

    expand=True,

    fill="x",

    padx=5
)


pass_value = tk.Label(

    card3,

    text="0%",

    font=(
        "Arial",
        20,
        "bold"
    )
)

pass_value.pack()


# Average attendance

card4 = tk.LabelFrame(

    dashboard_frame,

    text="Average Attendance",

    font=(
        "Arial",
        10,
        "bold"
    ),

    padx=30,

    pady=10
)

card4.pack(

    side="left",

    expand=True,

    fill="x",

    padx=5
)


attendance_value = tk.Label(

    card4,

    text="0%",

    font=(
        "Arial",
        20,
        "bold"
    )
)

attendance_value.pack()


# ==========================================
# INPUT FRAME
# ==========================================

input_frame = tk.LabelFrame(

    root,

    text="Student Data",

    font=(
        "Arial",
        12,
        "bold"
    ),

    padx=10,

    pady=10
)

input_frame.pack(

    fill="x",

    padx=20,

    pady=10
)


# Name

tk.Label(

    input_frame,

    text="Student Name"

).grid(

    row=0,

    column=0,

    padx=8,

    pady=8
)


name_entry = tk.Entry(

    input_frame,

    width=18
)

name_entry.grid(

    row=0,

    column=1,

    padx=8,

    pady=8
)


# Study

tk.Label(

    input_frame,

    text="Study Hours"

).grid(

    row=0,

    column=2,

    padx=8,

    pady=8
)


study_entry = tk.Entry(

    input_frame,

    width=14
)

study_entry.grid(

    row=0,

    column=3,

    padx=8,

    pady=8
)


# Attendance

tk.Label(

    input_frame,

    text="Attendance %"

).grid(

    row=0,

    column=4,

    padx=8,

    pady=8
)


attendance_entry = tk.Entry(

    input_frame,

    width=14
)

attendance_entry.grid(

    row=0,

    column=5,

    padx=8,

    pady=8
)


# Previous marks

tk.Label(

    input_frame,

    text="Previous Marks"

).grid(

    row=1,

    column=0,

    padx=8,

    pady=8
)


previous_entry = tk.Entry(

    input_frame,

    width=18
)

previous_entry.grid(

    row=1,

    column=1,

    padx=8,

    pady=8
)


# Final marks

tk.Label(

    input_frame,

    text="Final Marks"

).grid(

    row=1,

    column=2,

    padx=8,

    pady=8
)


final_entry = tk.Entry(

    input_frame,

    width=14
)

final_entry.grid(

    row=1,

    column=3,

    padx=8,

    pady=8
)


tk.Label(

    input_frame,

    text="Result: Automatic"

).grid(

    row=1,

    column=4,

    columnspan=2,

    padx=8,

    pady=8
)


# Add / Update button

add_button = tk.Button(

    input_frame,

    text="Add Student",

    width=18,

    command=add_student
)

add_button.grid(

    row=2,

    column=0,

    columnspan=2,

    pady=10
)


# Cancel button

cancel_button = tk.Button(

    input_frame,

    text="Cancel Edit",

    width=18,

    command=reset_edit_mode
)


# Clear button

tk.Button(

    input_frame,

    text="Clear",

    width=18,

    command=clear_inputs

).grid(

    row=2,

    column=2,

    columnspan=2,

    pady=10
)


# ==========================================
# SEARCH
# ==========================================

search_frame = tk.Frame(root)

search_frame.pack(

    fill="x",

    padx=20,

    pady=5
)


tk.Label(

    search_frame,

    text="Search Student:",

    font=(
        "Arial",
        10,
        "bold"
    )

).pack(
    side="left",
    padx=5
)


search_entry = tk.Entry(

    search_frame,

    width=30
)

search_entry.pack(

    side="left",

    padx=5
)


tk.Button(

    search_frame,

    text="Search",

    width=12,

    command=search_student

).pack(

    side="left",

    padx=5
)


tk.Button(

    search_frame,

    text="Show All",

    width=12,

    command=show_all_students

).pack(

    side="left",

    padx=5
)


# ==========================================
# TABLE
# ==========================================

table_frame = tk.Frame(root)

table_frame.pack(

    fill="both",

    expand=True,

    padx=20,

    pady=10
)


tree = ttk.Treeview(

    table_frame,

    columns=COLUMNS,

    show="headings",

    selectmode="browse"
)


widths = [

    180,

    110,

    170,

    140,

    120,

    100

]


for column, width in zip(

    COLUMNS,

    widths

):

    tree.heading(

        column,

        text=column
    )

    tree.column(

        column,

        width=width,

        anchor="center"
    )


vertical_scrollbar = ttk.Scrollbar(

    table_frame,

    orient="vertical",

    command=tree.yview
)


horizontal_scrollbar = ttk.Scrollbar(

    table_frame,

    orient="horizontal",

    command=tree.xview
)


tree.configure(

    yscrollcommand=vertical_scrollbar.set,

    xscrollcommand=horizontal_scrollbar.set
)


tree.pack(

    side="left",

    fill="both",

    expand=True
)


vertical_scrollbar.pack(

    side="right",

    fill="y"
)


horizontal_scrollbar.pack(

    side="bottom",

    fill="x"
)


# Double click = Student Details

tree.bind(

    "<Double-1>",

    lambda event: student_details()
)


# ==========================================
# MANAGEMENT BUTTONS
# ==========================================

management_frame = tk.Frame(root)

management_frame.pack(
    pady=8
)


tk.Button(

    management_frame,

    text="Edit Student",

    width=16,

    command=edit_student

).pack(

    side="left",

    padx=5
)


tk.Button(

    management_frame,

    text="Delete Student",

    width=16,

    command=delete_student

).pack(

    side="left",

    padx=5
)


tk.Button(

    management_frame,

    text="Student Details",

    width=18,

    command=student_details

).pack(

    side="left",

    padx=5
)


tk.Button(

    management_frame,

    text="Need Attention",

    width=18,

    command=students_needing_attention

).pack(

    side="left",

    padx=5
)


# ==========================================
# ANALYSIS BUTTONS
# ==========================================

analysis_button_frame = tk.Frame(root)

analysis_button_frame.pack(
    pady=8
)


tk.Button(

    analysis_button_frame,

    text="Refresh Data",

    width=18,

    command=refresh_table

).pack(

    side="left",

    padx=5
)


tk.Button(

    analysis_button_frame,

    text="Overall Analysis",

    width=18,

    command=overall_analysis

).pack(

    side="left",

    padx=5
)


tk.Button(

    analysis_button_frame,

    text="Top Student Analysis",

    width=22,

    command=top_student_analysis

).pack(

    side="left",

    padx=5
)


tk.Button(

    analysis_button_frame,

    text="Exit",

    width=15,

    command=root.destroy

).pack(

    side="left",

    padx=5
)


# ==========================================
# START APPLICATION
# ==========================================

refresh_table()

name_entry.focus()

root.mainloop()