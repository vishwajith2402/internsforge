import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess

from predict import predict_with_confidence
from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from job_matcher import calculate_match

from utils import model_exists

from candidate_database import (
    initialize_database,
    add_candidate,
    get_all_candidates,
    search_candidates,
    delete_candidate,
    get_statistics,
    get_candidate
)

from candidate_ranker import calculate_candidate_score

from report_generator import generate_report


# ============================================================
# COLORS
# ============================================================

BG = "#080B12"
SIDEBAR = "#0D111A"
PANEL = "#111827"
CARD = "#172033"
CARD2 = "#1E293B"

WHITE = "#F8FAFC"
GRAY = "#94A3B8"
MUTED = "#64748B"

PURPLE = "#7C3AED"
PURPLE_LIGHT = "#A78BFA"

CYAN = "#22D3EE"
GREEN = "#22C55E"
RED = "#EF4444"
ORANGE = "#F59E0B"

BORDER = "#293548"


# ============================================================
# MAIN APPLICATION
# ============================================================

class ResumeIQ:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "ResumeIQ - AI Resume Screening System"
        )

        self.root.geometry(
            "1450x900"
        )

        self.root.minsize(
            1200,
            750
        )

        self.root.configure(
            bg=BG
        )

        initialize_database()

        self.current_resume = ""
        self.current_file = ""
        self.current_skills = []

        self.current_prediction = ""
        self.current_confidence = 0

        self.current_match = {
            "overall_score": 0,
            "similarity_score": 0,
            "skill_score": 0,
            "matched_skills": [],
            "missing_skills": []
        }

        self.create_styles()
        self.create_layout()

        self.show_dashboard()


    # ========================================================
    # STYLES
    # ========================================================

    def create_styles(self):

        style = ttk.Style()

        try:
            style.theme_use(
                "clam"
            )
        except:
            pass

        style.configure(
            "Treeview",
            background=CARD,
            foreground=WHITE,
            fieldbackground=CARD,
            rowheight=34,
            borderwidth=0,
            font=(
                "Segoe UI",
                9
            )
        )

        style.configure(
            "Treeview.Heading",
            background=CARD2,
            foreground=WHITE,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[
                ("selected", PURPLE)
            ]
        )

        style.configure(
            "TScrollbar",
            background=CARD2,
            troughcolor=PANEL,
            arrowcolor=GRAY
        )


    # ========================================================
    # LAYOUT
    # ========================================================

    def create_layout(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=240
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        self.content = tk.Frame(
            self.root,
            bg=BG
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        logo = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )

        logo.pack(
            fill="x",
            padx=25,
            pady=(30, 35)
        )

        tk.Label(
            logo,
            text="Resume",
            font=(
                "Segoe UI",
                23,
                "bold"
            ),
            fg=WHITE,
            bg=SIDEBAR
        ).pack(
            side="left"
        )

        tk.Label(
            logo,
            text="IQ",
            font=(
                "Segoe UI",
                23,
                "bold"
            ),
            fg=CYAN,
            bg=SIDEBAR
        ).pack(
            side="left"
        )

        tk.Label(
            self.sidebar,
            text="AI RECRUITMENT INTELLIGENCE",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(
            padx=25,
            anchor="w",
            pady=(0, 12)
        )

        self.dashboard_button = self.sidebar_button(
            "⌂   Dashboard",
            self.show_dashboard
        )

        self.screen_button = self.sidebar_button(
            "◈   Screen Resume",
            self.show_screen
        )

        self.batch_button = self.sidebar_button(
            "▣   Batch Screening",
            self.show_batch
        )

        self.candidates_button = self.sidebar_button(
            "♙   Candidates",
            self.show_candidates
        )

        self.analytics_button = self.sidebar_button(
            "◉   Analytics",
            self.show_analytics
        )

        self.settings_button = self.sidebar_button(
            "⚙   System",
            self.show_system
        )

        spacer = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        self.model_status = tk.Label(
            self.sidebar,
            text="● Checking model...",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=GREEN,
            bg=SIDEBAR
        )

        self.model_status.pack(
            anchor="w",
            padx=25,
            pady=(0, 5)
        )

        tk.Label(
            self.sidebar,
            text="ResumeIQ v3.0",
            font=(
                "Segoe UI",
                8
            ),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

        self.update_model_status()


    # ========================================================
    # SIDEBAR BUTTON
    # ========================================================

    def sidebar_button(
        self,
        text,
        command
    ):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            bg=SIDEBAR,
            fg=GRAY,
            activebackground=CARD,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            pady=13,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            cursor="hand2"
        )

        button.pack(
            fill="x"
        )

        return button


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()


    # ========================================================
    # PAGE HEADER
    # ========================================================

    def page_header(
        self,
        title,
        subtitle
    ):

        header = tk.Frame(
            self.content,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(28, 20)
        )

        tk.Label(
            header,
            text=title,
            font=(
                "Segoe UI",
                25,
                "bold"
            ),
            fg=WHITE,
            bg=BG
        ).pack(
            anchor="w"
        )

        tk.Label(
            header,
            text=subtitle,
            font=(
                "Segoe UI",
                10
            ),
            fg=GRAY,
            bg=BG
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_content()

        self.page_header(
            "HR Dashboard",
            "AI-powered resume screening and candidate intelligence"
        )

        stats = get_statistics()

        cards = tk.Frame(
            self.content,
            bg=BG
        )

        cards.pack(
            fill="x",
            padx=35
        )

        self.stat_card(
            cards,
            "TOTAL CANDIDATES",
            str(
                stats["total_candidates"]
            ),
            CYAN
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.stat_card(
            cards,
            "AVERAGE MATCH",
            f'{stats["average_match"]:.1f}%',
            PURPLE_LIGHT
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.stat_card(
            cards,
            "SHORTLISTED",
            str(
                stats["shortlisted"]
            ),
            GREEN
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.stat_card(
            cards,
            "ML ENGINE",
            "ACTIVE" if model_exists()
            else "OFFLINE",
            GREEN if model_exists()
            else RED
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        # --------------------------------------------
        # QUICK ACTIONS
        # --------------------------------------------

        tk.Label(
            self.content,
            text="QUICK ACTIONS",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=GRAY,
            bg=BG
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 12)
        )

        actions = tk.Frame(
            self.content,
            bg=BG
        )

        actions.pack(
            fill="x",
            padx=35
        )

        self.action_card(
            actions,
            "Screen Resume",
            "Analyze one candidate using NLP + ML",
            self.show_screen
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.action_card(
            actions,
            "Batch Screening",
            "Screen multiple resumes simultaneously",
            self.show_batch
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.action_card(
            actions,
            "Candidate Ranking",
            "Compare candidates and find top talent",
            self.show_candidates
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        # --------------------------------------------
        # RECENT CANDIDATES
        # --------------------------------------------

        tk.Label(
            self.content,
            text="RECENT CANDIDATES",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=GRAY,
            bg=BG
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 10)
        )

        self.create_candidate_table(
            self.content,
            get_all_candidates()[:8]
        )


    # ========================================================
    # STAT CARD
    # ========================================================

    def stat_card(
        self,
        parent,
        title,
        value,
        accent
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            height=125
        )

        card.pack_propagate(
            False
        )

        tk.Frame(
            card,
            bg=accent,
            width=4
        ).pack(
            side="left",
            fill="y"
        )

        tk.Label(
            card,
            text=title,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=GRAY,
            bg=CARD
        ).pack(
            anchor="w",
            padx=18,
            pady=(22, 3)
        )

        tk.Label(
            card,
            text=value,
            font=(
                "Segoe UI",
                23,
                "bold"
            ),
            fg=WHITE,
            bg=CARD
        ).pack(
            anchor="w",
            padx=18
        )

        return card


    # ========================================================
    # ACTION CARD
    # ========================================================

    def action_card(
        self,
        parent,
        title,
        description,
        command
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            height=125,
            cursor="hand2"
        )

        card.pack_propagate(
            False
        )

        tk.Label(
            card,
            text=title,
            font=(
                "Segoe UI",
                14,
                "bold"
            ),
            fg=WHITE,
            bg=CARD
        ).pack(
            anchor="w",
            padx=20,
            pady=(22, 5)
        )

        tk.Label(
            card,
            text=description,
            font=(
                "Segoe UI",
                9
            ),
            fg=GRAY,
            bg=CARD,
            wraplength=240,
            justify="left"
        ).pack(
            anchor="w",
            padx=20
        )

        card.bind(
            "<Button-1>",
            lambda event: command()
        )

        return card


    # ========================================================
    # SCREEN RESUME PAGE
    # ========================================================

    def show_screen(self):

        self.clear_content()

        self.page_header(
            "Screen Resume",
            "Analyze a candidate using NLP, TF-IDF classification and skill matching"
        )

        main = tk.Frame(
            self.content,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=35
        )

        # LEFT
        left = tk.Frame(
            main,
            bg=PANEL
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # RIGHT
        right = tk.Frame(
            main,
            bg=PANEL,
            width=430
        )

        right.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        right.pack_propagate(
            False
        )

        # --------------------------------------------
        # UPLOAD
        # --------------------------------------------

        tk.Label(
            left,
            text="RESUME",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=GRAY,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 7)
        )

        upload_frame = tk.Frame(
            left,
            bg=PANEL
        )

        upload_frame.pack(
            fill="x",
            padx=20
        )

        self.make_button(
            upload_frame,
            "UPLOAD RESUME",
            self.upload_resume,
            PURPLE
        ).pack(
            side="left"
        )

        self.screen_file_label = tk.Label(
            upload_frame,
            text="No file selected",
            fg=GRAY,
            bg=PANEL,
            font=(
                "Segoe UI",
                9
            )
        )

        self.screen_file_label.pack(
            side="left",
            padx=12
        )

        # --------------------------------------------
        # RESUME TEXT
        # --------------------------------------------

        self.screen_resume_box = tk.Text(
            left,
            bg=CARD,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            wrap="word",
            font=(
                "Segoe UI",
                10
            ),
            padx=15,
            pady=15
        )

        self.screen_resume_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=12
        )

        # --------------------------------------------
        # JOB DESCRIPTION
        # --------------------------------------------

        tk.Label(
            left,
            text="JOB DESCRIPTION",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=GRAY,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=20
        )

        self.screen_job_box = tk.Text(
            left,
            height=7,
            bg=CARD,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            wrap="word",
            font=(
                "Segoe UI",
                9
            ),
            padx=15,
            pady=12
        )

        self.screen_job_box.pack(
            fill="x",
            padx=20,
            pady=10
        )

        button_frame = tk.Frame(
            left,
            bg=PANEL
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.make_button(
            button_frame,
            "ANALYZE CANDIDATE",
            self.analyze_candidate,
            PURPLE
        ).pack(
            side="left"
        )

        self.make_button(
            button_frame,
            "SAVE CANDIDATE",
            self.save_current_candidate,
            GREEN
        ).pack(
            side="left",
            padx=10
        )

        # --------------------------------------------
        # RESULT CARD
        # --------------------------------------------

        tk.Label(
            right,
            text="AI SCREENING RESULT",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=GRAY,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 12)
        )

        self.screen_role = self.result_value(
            right,
            "PREDICTED ROLE"
        )

        self.screen_confidence = self.result_value(
            right,
            "MODEL CONFIDENCE"
        )

        self.screen_match = self.result_value(
            right,
            "JOB MATCH"
        )

        self.screen_similarity = self.result_value(
            right,
            "TEXT SIMILARITY"
        )

        self.screen_skill_score = self.result_value(
            right,
            "SKILL MATCH"
        )

        # --------------------------------------------
        # SKILLS
        # --------------------------------------------

        tk.Label(
            right,
            text="DETECTED SKILLS",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=GRAY,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 5)
        )

        self.screen_skills = tk.Label(
            right,
            text="—",
            fg=CYAN,
            bg=PANEL,
            font=(
                "Segoe UI",
                9
            ),
            wraplength=370,
            justify="left"
        )

        self.screen_skills.pack(
            anchor="w",
            padx=22
        )

        # --------------------------------------------
        # SKILL GAP
        # --------------------------------------------

        tk.Label(
            right,
            text="SKILL GAP",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=GRAY,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 5)
        )

        self.screen_missing = tk.Label(
            right,
            text="—",
            fg=RED,
            bg=PANEL,
            font=(
                "Segoe UI",
                9
            ),
            wraplength=370,
            justify="left"
        )

        self.screen_missing.pack(
            anchor="w",
            padx=22
        )

        self.make_button(
            right,
            "GENERATE PDF REPORT",
            self.generate_current_report,
            CARD2
        ).pack(
            fill="x",
            padx=22,
            pady=25
        )


    # ========================================================
    # UPLOAD
    # ========================================================

    def upload_resume(self):

        path = filedialog.askopenfilename(

            title="Select Resume",

            filetypes=[
                (
                    "Resume Files",
                    "*.pdf *.docx *.txt"
                ),
                (
                    "PDF",
                    "*.pdf"
                ),
                (
                    "Word",
                    "*.docx"
                ),
                (
                    "Text",
                    "*.txt"
                )
            ]
        )

        if not path:
            return

        try:

            text = extract_resume_text(
                path
            )

            if not text.strip():

                raise ValueError(
                    "No readable text was found."
                )

            self.current_file = path
            self.current_resume = text

            self.screen_resume_box.delete(
                "1.0",
                "end"
            )

            self.screen_resume_box.insert(
                "1.0",
                text
            )

            self.screen_file_label.config(
                text=os.path.basename(path),
                fg=CYAN
            )

            self.current_skills = extract_skills(
                text
            )

            self.screen_skills.config(
                text=", ".join(
                    self.current_skills
                )
                if self.current_skills
                else "No skills detected."
            )

        except Exception as error:

            messagebox.showerror(
                "Resume Error",
                str(error)
            )


    # ========================================================
    # ANALYZE
    # ========================================================

    def analyze_candidate(self):

        if not model_exists():

            messagebox.showwarning(
                "Model Missing",
                "Train the ML model first."
            )

            return

        resume = self.screen_resume_box.get(
            "1.0",
            "end"
        ).strip()

        job = self.screen_job_box.get(
            "1.0",
            "end"
        ).strip()

        if not resume:

            messagebox.showwarning(
                "Resume Required",
                "Upload or paste a resume."
            )

            return

        try:

            self.current_resume = resume

            self.current_skills = extract_skills(
                resume
            )

            role, confidence = predict_with_confidence(
                resume,
                ", ".join(
                    self.current_skills
                ),
                "",
                ""
            )

            self.current_prediction = role
            self.current_confidence = float(
                confidence or 0
            )

            self.screen_role.config(
                text=role
            )

            self.screen_confidence.config(
                text=f"{self.current_confidence:.1f}%"
            )

            self.screen_skills.config(
                text=", ".join(
                    self.current_skills
                )
                if self.current_skills
                else "No skills detected."
            )

            if job:

                match = calculate_match(
                    resume,
                    job
                )

                self.current_match = match

                self.screen_match.config(
                    text=f'{match["overall_score"]:.1f}%'
                )

                self.screen_similarity.config(
                    text=f'{match["similarity_score"]:.1f}%'
                )

                self.screen_skill_score.config(
                    text=f'{match["skill_score"]:.1f}%'
                )

                missing = match[
                    "missing_skills"
                ]

                self.screen_missing.config(
                    text=", ".join(
                        missing
                    )
                    if missing
                    else "No major skill gaps."
                )

            else:

                self.screen_match.config(
                    text="—"
                )

                self.screen_similarity.config(
                    text="—"
                )

                self.screen_skill_score.config(
                    text="—"
                )

                self.screen_missing.config(
                    text="Add a job description for skill-gap analysis."
                )

            messagebox.showinfo(
                "Analysis Complete",
                "Candidate analysis completed successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Analysis Error",
                str(error)
            )


    # ========================================================
    # SAVE CANDIDATE
    # ========================================================

    def save_current_candidate(self):

        if not self.current_resume:

            messagebox.showwarning(
                "No Candidate",
                "Analyze a resume first."
            )

            return

        name = self.extract_candidate_name(
            self.current_resume
        )

        match = self.current_match

        match_score = float(
            match.get(
                "overall_score",
                0
            )
        )

        resume_score = self.calculate_resume_score(
            self.current_resume,
            self.current_skills
        )

        candidate_id = add_candidate(

            name,

            self.current_file,

            self.current_prediction,

            self.current_confidence,

            resume_score,

            match_score,

            float(
                match.get(
                    "similarity_score",
                    0
                )
            ),

            float(
                match.get(
                    "skill_score",
                    0
                )
            ),

            self.current_skills,

            match.get(
                "matched_skills",
                []
            ),

            match.get(
                "missing_skills",
                []
            )
        )

        messagebox.showinfo(
            "Candidate Saved",
            f"Candidate saved successfully.\n\n"
            f"Candidate ID: {candidate_id}"
        )

        self.show_candidates()


    # ========================================================
    # CANDIDATE NAME
    # ========================================================

    def extract_candidate_name(
        self,
        text
    ):

        lines = [

            line.strip()

            for line in text.splitlines()

            if line.strip()
        ]

        if lines:

            first = lines[0]

            if (
                len(first) < 80
                and "@" not in first
                and not any(
                    character.isdigit()
                    for character in first
                )
            ):

                return first

        return "Unknown Candidate"


    # ========================================================
    # RESUME SCORE
    # ========================================================

    def calculate_resume_score(
        self,
        resume,
        skills
    ):

        score = 0

        if len(resume) > 500:
            score += 25

        if len(resume) > 1200:
            score += 15

        if len(skills) >= 3:
            score += 20

        if len(skills) >= 7:
            score += 15

        lower = resume.lower()

        if "education" in lower:
            score += 10

        if "experience" in lower:
            score += 10

        if "project" in lower:
            score += 5

        return min(
            score,
            100
        )


    # ========================================================
    # BATCH PAGE
    # ========================================================

    def show_batch(self):

        self.clear_content()

        self.page_header(
            "Batch Screening",
            "Screen multiple resumes against a single job description"
        )

        top = tk.Frame(
            self.content,
            bg=PANEL
        )

        top.pack(
            fill="x",
            padx=35
        )

        tk.Label(
            top,
            text="JOB DESCRIPTION",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=GRAY,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.batch_job_box = tk.Text(
            top,
            height=7,
            bg=CARD,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            wrap="word",
            font=(
                "Segoe UI",
                9
            ),
            padx=12,
            pady=10
        )

        self.batch_job_box.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        buttons = tk.Frame(
            top,
            bg=PANEL
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.make_button(
            buttons,
            "SELECT RESUME FILES",
            self.batch_select_files,
            PURPLE
        ).pack(
            side="left"
        )

        self.make_button(
            buttons,
            "SELECT RESUME FOLDER",
            self.batch_select_folder,
            CARD2
        ).pack(
            side="left",
            padx=10
        )

        self.batch_count_label = tk.Label(
            buttons,
            text="No resumes selected",
            fg=GRAY,
            bg=PANEL
        )

        self.batch_count_label.pack(
            side="left",
            padx=15
        )

        self.batch_files = []

        # --------------------------------------------
        # RESULTS
        # --------------------------------------------

        result_frame = tk.Frame(
            self.content,
            bg=PANEL
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        columns = (
            "rank",
            "candidate",
            "role",
            "match",
            "skills",
            "final"
        )

        self.batch_table = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "rank": "#",
            "candidate": "Candidate",
            "role": "Predicted Role",
            "match": "Job Match",
            "skills": "Skills",
            "final": "Final Score"
        }

        widths = {
            "rank": 50,
            "candidate": 220,
            "role": 180,
            "match": 120,
            "skills": 120,
            "final": 120
        }

        for column in columns:

            self.batch_table.heading(
                column,
                text=headings[column]
            )

            self.batch_table.column(
                column,
                width=widths[column]
            )

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.batch_table.yview
        )

        self.batch_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.batch_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


    # ========================================================
    # SELECT FILES
    # ========================================================

    def batch_select_files(self):

        files = filedialog.askopenfilenames(

            title="Select Resumes",

            filetypes=[
                (
                    "Resume Files",
                    "*.pdf *.docx *.txt"
                )
            ]
        )

        if files:

            self.batch_files = list(
                files
            )

            self.batch_count_label.config(
                text=f"{len(files)} resumes selected",
                fg=CYAN
            )

            self.run_batch_screening()


    # ========================================================
    # SELECT FOLDER
    # ========================================================

    def batch_select_folder(self):

        folder = filedialog.askdirectory(
            title="Select Resume Folder"
        )

        if not folder:
            return

        supported = (
            ".pdf",
            ".docx",
            ".txt"
        )

        self.batch_files = [

            os.path.join(
                folder,
                filename
            )

            for filename in os.listdir(
                folder
            )

            if filename.lower().endswith(
                supported
            )
        ]

        self.batch_count_label.config(
            text=f"{len(self.batch_files)} resumes found",
            fg=CYAN
        )

        self.run_batch_screening()


    # ========================================================
    # BATCH SCREENING
    # ========================================================

    def run_batch_screening(self):

        job = self.batch_job_box.get(
            "1.0",
            "end"
        ).strip()

        if not job:

            messagebox.showwarning(
                "Job Description",
                "Enter a job description first."
            )

            return

        if not self.batch_files:

            return

        for item in self.batch_table.get_children():

            self.batch_table.delete(
                item
            )

        ranked_results = []

        for path in self.batch_files:

            try:

                text = extract_resume_text(
                    path
                )

                skills = extract_skills(
                    text
                )

                role, confidence = predict_with_confidence(
                    text,
                    ", ".join(
                        skills
                    ),
                    "",
                    ""
                )

                match = calculate_match(
                    text,
                    job
                )

                resume_score = self.calculate_resume_score(
                    text,
                    skills
                )

                final_score = calculate_candidate_score(
                    match.get(
                        "overall_score",
                        0
                    ),
                    resume_score,
                    confidence
                )

                name = self.extract_candidate_name(
                    text
                )

                candidate_data = {

                    "name": name,

                    "role": role,

                    "match": match.get(
                        "overall_score",
                        0
                    ),

                    "skills": len(
                        skills
                    ),

                    "final": final_score,

                    "path": path,

                    "confidence": confidence,

                    "resume_score": resume_score,

                    "similarity": match.get(
                        "similarity_score",
                        0
                    ),

                    "skill_score": match.get(
                        "skill_score",
                        0
                    ),

                    "skill_list": skills,

                    "matched": match.get(
                        "matched_skills",
                        []
                    ),

                    "missing": match.get(
                        "missing_skills",
                        []
                    )
                }

                ranked_results.append(
                    candidate_data
                )

            except Exception as error:

                print(
                    f"Error processing "
                    f"{os.path.basename(path)}: "
                    f"{error}"
                )

        ranked_results.sort(
            key=lambda x: x["final"],
            reverse=True
        )

        for rank, candidate in enumerate(
            ranked_results,
            start=1
        ):

            self.batch_table.insert(
                "",
                "end",
                values=(

                    rank,

                    candidate["name"],

                    candidate["role"],

                    f'{candidate["match"]:.1f}%',

                    candidate["skills"],

                    f'{candidate["final"]:.1f}%'
                )
            )

        self.batch_results = ranked_results

        messagebox.showinfo(
            "Batch Screening Complete",
            f"Processed {len(ranked_results)} resumes."
        )


    # ========================================================
    # CANDIDATES PAGE
    # ========================================================

    def show_candidates(self):

        self.clear_content()

        self.page_header(
            "Candidate Database",
            "Search, rank and manage screened candidates"
        )

        search_frame = tk.Frame(
            self.content,
            bg=BG
        )

        search_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 15)
        )

        tk.Label(
            search_frame,
            text="SEARCH",
            fg=GRAY,
            bg=BG,
            font=(
                "Segoe UI",
                8,
                "bold"
            )
        ).pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            search_frame,
            bg=CARD,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=(
                "Segoe UI",
                10
            )
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            ipady=9
        )

        self.make_button(
            search_frame,
            "SEARCH",
            self.search_database,
            PURPLE
        ).pack(
            side="left"
        )

        self.make_button(
            search_frame,
            "REFRESH",
            self.show_candidates,
            CARD2
        ).pack(
            side="left",
            padx=8
        )

        self.make_button(
            search_frame,
            "DELETE SELECTED",
            self.delete_selected_candidate,
            RED
        ).pack(
            side="left"
        )

        self.create_candidate_table(
            self.content,
            get_all_candidates()
        )


    # ========================================================
    # CANDIDATE TABLE
    # ========================================================

    def create_candidate_table(
        self,
        parent,
        candidates
    ):

        frame = tk.Frame(
            parent,
            bg=PANEL
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )

        columns = (
            "id",
            "name",
            "role",
            "match",
            "confidence",
            "final"
        )

        self.candidate_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        headings = {

            "id": "ID",

            "name": "Candidate",

            "role": "Predicted Role",

            "match": "Job Match",

            "confidence": "ML Confidence",

            "final": "Ranking Score"
        }

        widths = {

            "id": 60,

            "name": 250,

            "role": 220,

            "match": 140,

            "confidence": 150,

            "final": 160
        }

        for column in columns:

            self.candidate_table.heading(
                column,
                text=headings[column]
            )

            self.candidate_table.column(
                column,
                width=widths[column]
            )

        for candidate in candidates:

            final_score = calculate_candidate_score(

                candidate["match_score"],

                candidate["resume_score"],

                candidate["confidence"]
            )

            self.candidate_table.insert(
                "",
                "end",
                values=(

                    candidate["id"],

                    candidate["candidate_name"],

                    candidate["predicted_role"],

                    f'{candidate["match_score"]:.1f}%',

                    f'{candidate["confidence"]:.1f}%',

                    f'{final_score:.1f}%'
                )
            )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.candidate_table.yview
        )

        self.candidate_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.candidate_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


    # ========================================================
    # SEARCH DATABASE
    # ========================================================

    def search_database(self):

        keyword = self.search_entry.get().strip()

        if not keyword:

            self.show_candidates()

            return

        self.clear_candidate_table()

        candidates = search_candidates(
            keyword
        )

        for candidate in candidates:

            final_score = calculate_candidate_score(

                candidate["match_score"],

                candidate["resume_score"],

                candidate["confidence"]
            )

            self.candidate_table.insert(
                "",
                "end",
                values=(

                    candidate["id"],

                    candidate["candidate_name"],

                    candidate["predicted_role"],

                    f'{candidate["match_score"]:.1f}%',

                    f'{candidate["confidence"]:.1f}%',

                    f'{final_score:.1f}%'
                )
            )


    # ========================================================
    # CLEAR TABLE
    # ========================================================

    def clear_candidate_table(self):

        if not hasattr(
            self,
            "candidate_table"
        ):
            return

        for item in self.candidate_table.get_children():

            self.candidate_table.delete(
                item
            )


    # ========================================================
    # DELETE CANDIDATE
    # ========================================================

    def delete_selected_candidate(self):

        if not hasattr(
            self,
            "candidate_table"
        ):
            return

        selected = self.candidate_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Candidate",
                "Select a candidate first."
            )

            return

        values = self.candidate_table.item(
            selected[0],
            "values"
        )

        candidate_id = values[0]

        confirm = messagebox.askyesno(
            "Delete Candidate",
            "Are you sure you want to delete this candidate?"
        )

        if confirm:

            delete_candidate(
                candidate_id
            )

            self.show_candidates()


    # ========================================================
    # ANALYTICS
    # ========================================================

    def show_analytics(self):

        self.clear_content()

        self.page_header(
            "HR Analytics",
            "Candidate screening statistics and recruitment intelligence"
        )

        stats = get_statistics()

        container = tk.Frame(
            self.content,
            bg=BG
        )

        container.pack(
            fill="both",
            expand=True,
            padx=35
        )

        # --------------------------------------------
        # STATISTICS
        # --------------------------------------------

        candidates = get_all_candidates()

        total = len(
            candidates
        )

        shortlisted = len([

            c

            for c in candidates

            if c["match_score"] >= 70
        ])

        high_match = len([

            c

            for c in candidates

            if c["match_score"] >= 80
        ])

        average_confidence = (

            sum(
                c["confidence"]
                for c in candidates
            )
            / total

            if total
            else 0
        )

        row = tk.Frame(
            container,
            bg=BG
        )

        row.pack(
            fill="x"
        )

        self.stat_card(
            row,
            "TOTAL SCREENED",
            str(total),
            CYAN
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.stat_card(
            row,
            "SHORTLISTED",
            str(shortlisted),
            GREEN
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.stat_card(
            row,
            "HIGH MATCH",
            str(high_match),
            PURPLE_LIGHT
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.stat_card(
            row,
            "AVG ML CONFIDENCE",
            f"{average_confidence:.1f}%",
            ORANGE
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        # --------------------------------------------
        # INTERPRETATION
        # --------------------------------------------

        analysis = tk.Frame(
            container,
            bg=PANEL
        )

        analysis.pack(
            fill="x",
            pady=25
        )

        tk.Label(
            analysis,
            text="SCREENING INSIGHTS",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=WHITE,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        if total == 0:

            insight = (
                "No candidates have been screened yet. "
                "Use Batch Screening or Screen Resume "
                "to start building your recruitment database."
            )

        else:

            percentage = (
                shortlisted / total
            ) * 100

            insight = (
                f"{total} candidate(s) have been screened. "
                f"{shortlisted} candidate(s) currently meet "
                f"the 70% shortlist threshold "
                f"({percentage:.1f}%). "
                f"{high_match} candidate(s) have an "
                f"80%+ job match."
            )

        tk.Label(
            analysis,
            text=insight,
            font=(
                "Segoe UI",
                11
            ),
            fg=GRAY,
            bg=PANEL,
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )


    # ========================================================
    # SYSTEM
    # ========================================================

    def show_system(self):

        self.clear_content()

        self.page_header(
            "System",
            "Machine learning model and application controls"
        )

        panel = tk.Frame(
            self.content,
            bg=PANEL
        )

        panel.pack(
            fill="x",
            padx=35
        )

        status = (
            "MODEL READY"
            if model_exists()
            else "MODEL NOT TRAINED"
        )

        color = (
            GREEN
            if model_exists()
            else RED
        )

        tk.Label(
            panel,
            text=status,
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            fg=color,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            panel,
            text=(
                "ResumeIQ uses NLP + TF-IDF + machine "
                "learning classification for resume screening."
            ),
            fg=GRAY,
            bg=PANEL,
            font=(
                "Segoe UI",
                10
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

        buttons = tk.Frame(
            panel,
            bg=PANEL
        )

        buttons.pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

        self.make_button(
            buttons,
            "TRAIN / RETRAIN MODEL",
            self.train_model,
            PURPLE
        ).pack(
            side="left"
        )

        self.make_button(
            buttons,
            "RUN EVALUATION",
            self.run_evaluation,
            CARD2
        ).pack(
            side="left",
            padx=10
        )


    # ========================================================
    # TRAIN MODEL
    # ========================================================

    def train_model(self):

        try:

            result = subprocess.run(

                [
                    sys.executable,
                    "train_model.py"
                ],

                capture_output=True,

                text=True
            )

            if result.returncode != 0:

                messagebox.showerror(
                    "Training Error",
                    result.stderr
                )

                return

            self.update_model_status()

            messagebox.showinfo(
                "Training Complete",
                "The ML model was trained successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Training Error",
                str(error)
            )


    # ========================================================
    # EVALUATION
    # ========================================================

    def run_evaluation(self):

        try:

            result = subprocess.run(

                [
                    sys.executable,
                    "evaluation.py"
                ],

                capture_output=True,

                text=True
            )

            if result.returncode != 0:

                messagebox.showerror(
                    "Evaluation Error",
                    result.stderr
                )

                return

            messagebox.showinfo(
                "Evaluation Complete",
                "Model evaluation completed.\n\n"
                "Check the outputs folder."
            )

        except Exception as error:

            messagebox.showerror(
                "Evaluation Error",
                str(error)
            )


    # ========================================================
    # RESULT VALUE
    # ========================================================

    def result_value(
        self,
        parent,
        title
    ):

        frame = tk.Frame(
            parent,
            bg=CARD
        )

        frame.pack(
            fill="x",
            padx=22,
            pady=5
        )

        tk.Label(
            frame,
            text=title,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=GRAY,
            bg=CARD
        ).pack(
            anchor="w",
            padx=12,
            pady=(9, 0)
        )

        value = tk.Label(
            frame,
            text="—",
            font=(
                "Segoe UI",
                16,
                "bold"
            ),
            fg=CYAN,
            bg=CARD
        )

        value.pack(
            anchor="w",
            padx=12,
            pady=(1, 9)
        )

        return value


    # ========================================================
    # BUTTON
    # ========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        background
    ):

        return tk.Button(

            parent,

            text=text,

            command=command,

            bg=background,

            fg=WHITE,

            activebackground=PURPLE,

            activeforeground=WHITE,

            relief="flat",

            bd=0,

            font=(
                "Segoe UI",
                9,
                "bold"
            ),

            padx=15,

            pady=9,

            cursor="hand2"
        )


    # ========================================================
    # PDF REPORT
    # ========================================================

    def generate_current_report(self):

        if not self.current_resume:

            messagebox.showwarning(
                "No Candidate",
                "Analyze a resume first."
            )

            return

        try:

            name = self.extract_candidate_name(
                self.current_resume
            )

            match = self.current_match

            resume_score = self.calculate_resume_score(
                self.current_resume,
                self.current_skills
            )

            path = generate_report(

                name,

                self.current_prediction,

                self.current_confidence,

                resume_score,

                match.get(
                    "overall_score",
                    0
                ),

                match.get(
                    "similarity_score",
                    0
                ),

                match.get(
                    "skill_score",
                    0
                ),

                self.current_skills,

                match.get(
                    "matched_skills",
                    []
                ),

                match.get(
                    "missing_skills",
                    []
                )
            )

            messagebox.showinfo(
                "Report Generated",
                f"PDF report created successfully.\n\n"
                f"{path}"
            )

        except Exception as error:

            messagebox.showerror(
                "Report Error",
                str(error)
            )


    # ========================================================
    # MODEL STATUS
    # ========================================================

    def update_model_status(self):

        if model_exists():

            self.model_status.config(
                text="● ML MODEL READY",
                fg=GREEN
            )

        else:

            self.model_status.config(
                text="● MODEL NOT TRAINED",
                fg=RED
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    application = ResumeIQ(
        root
    )

    root.mainloop()