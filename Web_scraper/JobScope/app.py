import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import json
from urllib.parse import urlparse

# Selenium is optional at runtime.
# The app can still use Requests + BeautifulSoup if Selenium fails.
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    SELENIUM_AVAILABLE = True

except ImportError:
    SELENIUM_AVAILABLE = False


# ============================================================
# JOBSCOPE
# Web Scraping + Job Market Analysis
# Single-file application
# ============================================================


# ============================================================
# COLORS
# ============================================================

BG = "#08090D"
PANEL = "#11131C"
PANEL_2 = "#181B27"

PURPLE = "#7C3AED"
PURPLE_DARK = "#4C1D95"

CYAN = "#22D3EE"
GREEN = "#34D399"
RED = "#FB7185"

WHITE = "#F8FAFC"
TEXT = "#CBD5E1"
MUTED = "#94A3B8"


# ============================================================
# JOB SCRAPER
# ============================================================

class JobScraper:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/153.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9"
        })

        self.skills = [
            "Python",
            "Java",
            "C++",
            "C#",
            "JavaScript",
            "TypeScript",
            "Go",
            "Rust",
            "SQL",
            "MySQL",
            "PostgreSQL",
            "MongoDB",
            "Redis",
            "Machine Learning",
            "Deep Learning",
            "Artificial Intelligence",
            "Data Science",
            "Data Analytics",
            "Power BI",
            "Tableau",
            "TensorFlow",
            "PyTorch",
            "AWS",
            "Azure",
            "Google Cloud",
            "Docker",
            "Kubernetes",
            "Git",
            "GitHub",
            "React",
            "Node.js",
            "Django",
            "Flask",
            "FastAPI",
            "HTML",
            "CSS",
            "NLP",
            "Excel",
            "Spark",
            "Hadoop",
            "Kafka",
            "Airflow",
            "Linux"
        ]


    # ========================================================
    # MAIN URL ROUTER
    # ========================================================

    def scan_url(self, url):

        url = url.strip()

        if not url:
            raise ValueError(
                "Please enter a URL."
            )

        if not url.startswith(
            ("http://", "https://")
        ):
            raise ValueError(
                "URL must start with http:// or https://"
            )

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        # --------------------------------------------
        # REMOTIVE
        # --------------------------------------------

        if "remotive.com" in domain:

            return self.scan_remotive(
                url
            )

        # --------------------------------------------
        # NORMAL HTML
        # --------------------------------------------

        html = self.fetch_html(
            url
        )

        jobs = self.parse_html_jobs(
            html,
            url
        )

        # --------------------------------------------
        # FALLBACK TO SELENIUM
        # --------------------------------------------

        if len(jobs) == 0:

            if not SELENIUM_AVAILABLE:

                raise ValueError(
                    "No jobs found in the HTML page.\n\n"
                    "This website may require JavaScript.\n\n"
                    "Install Selenium with:\n"
                    "python -m pip install selenium"
                )

            html = self.fetch_with_selenium(
                url
            )

            jobs = self.parse_html_jobs(
                html,
                url
            )

        if not jobs:

            raise ValueError(
                "The page was loaded, but JobScope "
                "could not identify job listings.\n\n"
                "This website may use a custom layout "
                "or protected content."
            )

        return jobs


    # ========================================================
    # REMOTIVE API
    # ========================================================

    def scan_remotive(
        self,
        url
    ):

        parsed = urlparse(
            url
        )

        path = parsed.path.lower()

        # Direct API URL
        if "/api/" in path:

            api_url = url

        else:

            api_url = (
                "https://remotive.com/"
                "api/remote-jobs"
            )

            # Try to extract useful search text
            # from URLs like:
            # /remote-jobs/o-python-developer

            parts = [
                part
                for part in path.split("/")
                if part
            ]

            if parts:

                possible_search = (
                    parts[-1]
                    .replace(
                        "remote-jobs",
                        ""
                    )
                    .replace(
                        "o-",
                        ""
                    )
                    .replace(
                        "-",
                        " "
                    )
                    .strip()
                )

                if possible_search:

                    response = self.session.get(
                        api_url,
                        params={
                            "search": possible_search,
                            "limit": 50
                        },
                        timeout=20
                    )

                else:

                    response = self.session.get(
                        api_url,
                        params={
                            "limit": 50
                        },
                        timeout=20
                    )

            else:

                response = self.session.get(
                    api_url,
                    params={
                        "limit": 50
                    },
                    timeout=20
                )

        if "response" not in locals():

            response = self.session.get(
                api_url,
                timeout=20
            )

        response.raise_for_status()

        try:

            data = response.json()

        except json.JSONDecodeError:

            raise ValueError(
                "Remotive returned an unexpected response."
            )

        jobs = data.get(
            "jobs",
            []
        )

        if not jobs:

            raise ValueError(
                "Remotive returned no matching jobs."
            )

        normalized = []

        for job in jobs:

            title = job.get(
                "title",
                "Not Specified"
            )

            company = job.get(
                "company_name",
                "Not Specified"
            )

            location = job.get(
                "candidate_required_location",
                "Remote"
            )

            salary = job.get(
                "salary",
                "Not Specified"
            )

            description = BeautifulSoup(
                job.get(
                    "description",
                    ""
                ),
                "html.parser"
            ).get_text(
                " ",
                strip=True
            )

            tags = job.get(
                "tags",
                []
            )

            skills_text = ", ".join(
                tags
            )

            detected_skills = self.extract_skills(
                description + " " + skills_text
            )

            if detected_skills == "Not Specified":
                detected_skills = skills_text or "Not Specified"

            experience = self.extract_experience(
                description
            )

            normalized.append({
                "Job Title": title,
                "Company Name": company,
                "Location": location,
                "Experience": experience,
                "Skills": detected_skills,
                "Salary": salary,
                "Source": "Remotive",
                "Job URL": job.get(
                    "url",
                    ""
                )
            })

        return normalized


    # ========================================================
    # REQUESTS HTML
    # ========================================================

    def fetch_html(
        self,
        url
    ):

        response = self.session.get(
            url,
            timeout=20,
            allow_redirects=True
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if (
            "text/html" not in content_type
            and "application/xhtml" not in content_type
        ):

            raise ValueError(
                "The URL did not return an HTML page."
            )

        return response.text


    # ========================================================
    # SELENIUM
    # ========================================================

    def fetch_with_selenium(
        self,
        url
    ):

        if not SELENIUM_AVAILABLE:

            raise RuntimeError(
                "Selenium is not installed."
            )

        options = Options()

        options.add_argument(
            "--headless=new"
        )

        options.add_argument(
            "--disable-gpu"
        )

        options.add_argument(
            "--no-sandbox"
        )

        options.add_argument(
            "--disable-dev-shm-usage"
        )

        options.add_argument(
            "--window-size=1920,1080"
        )

        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        driver = None

        try:

            driver = webdriver.Chrome(
                options=options
            )

            driver.get(
                url
            )

            try:

                WebDriverWait(
                    driver,
                    10
                ).until(
                    EC.presence_of_element_located(
                        (
                            By.TAG_NAME,
                            "body"
                        )
                    )
                )

            except Exception:
                pass

            # Give JavaScript applications
            # additional time to render.
            import time

            time.sleep(3)

            html = driver.page_source

            return html

        finally:

            if driver:

                driver.quit()


    # ========================================================
    # HTML JOB PARSER
    # ========================================================

    def parse_html_jobs(
        self,
        html,
        source_url=""
    ):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        jobs = []

        # --------------------------------------------
        # Strategy 1: JSON-LD
        # --------------------------------------------

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for script in scripts:

            try:

                data = json.loads(
                    script.string or
                    script.get_text()
                )

                if isinstance(
                    data,
                    dict
                ):

                    if data.get(
                        "@type"
                    ) == "JobPosting":

                        jobs.append(
                            self.normalize_jobposting(
                                data
                            )
                        )

                    elif isinstance(
                        data.get("itemListElement"),
                        list
                    ):

                        for item in data[
                            "itemListElement"
                        ]:

                            posting = item.get(
                                "item",
                                item
                            )

                            if isinstance(
                                posting,
                                dict
                            ):

                                if posting.get(
                                    "@type"
                                ) == "JobPosting":

                                    jobs.append(
                                        self.normalize_jobposting(
                                            posting
                                        )
                                    )

            except Exception:

                continue

        # --------------------------------------------
        # Strategy 2: common job-card selectors
        # --------------------------------------------

        selectors = [
            "article",
            "[data-job-id]",
            "[data-job]",
            ".job-card",
            ".job-listing",
            ".job-item",
            ".job",
            ".job-result",
            ".job-card-container",
            ".job-search-card"
        ]

        cards = []

        for selector in selectors:

            try:

                found = soup.select(
                    selector
                )

                cards.extend(
                    found
                )

            except Exception:

                continue

        # Remove duplicates
        unique_cards = []

        seen = set()

        for card in cards:

            text = card.get_text(
                " ",
                strip=True
            )

            identifier = (
                text[:500]
            )

            if (
                identifier
                and identifier not in seen
            ):

                seen.add(
                    identifier
                )

                unique_cards.append(
                    card
                )

        for card in unique_cards:

            title = self.find_from_selectors(
                card,
                [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    ".job-title",
                    ".job-title-link",
                    ".title",
                    "[class*='job-title']",
                    "[class*='job_title']"
                ]
            )

            if not title:
                continue

            company = self.find_from_selectors(
                card,
                [
                    ".company",
                    ".company-name",
                    ".employer",
                    "[class*='company']",
                    "[class*='employer']"
                ]
            )

            location = self.find_from_selectors(
                card,
                [
                    ".location",
                    ".job-location",
                    "[class*='location']"
                ]
            )

            text = card.get_text(
                " ",
                strip=True
            )

            experience = self.extract_experience(
                text
            )

            salary = self.extract_salary(
                text
            )

            skills = self.extract_skills(
                text
            )

            jobs.append({
                "Job Title": title,
                "Company Name": company or "Not Specified",
                "Location": location or "Not Specified",
                "Experience": experience,
                "Skills": skills,
                "Salary": salary,
                "Source": urlparse(
                    source_url
                ).netloc if source_url else "Web",
                "Job URL": source_url
            })

        # --------------------------------------------
        # Remove duplicate jobs
        # --------------------------------------------

        final_jobs = []

        seen_jobs = set()

        for job in jobs:

            key = (
                job.get(
                    "Job Title",
                    ""
                ).lower(),
                job.get(
                    "Company Name",
                    ""
                ).lower()
            )

            if key not in seen_jobs:

                seen_jobs.add(
                    key
                )

                final_jobs.append(
                    job
                )

        return final_jobs


    # ========================================================
    # JSON-LD NORMALIZATION
    # ========================================================

    def normalize_jobposting(
        self,
        data
    ):

        title = data.get(
            "title",
            "Not Specified"
        )

        company_data = data.get(
            "hiringOrganization",
            {}
        )

        if isinstance(
            company_data,
            dict
        ):

            company = company_data.get(
                "name",
                "Not Specified"
            )

        else:

            company = str(
                company_data
            )

        location_data = data.get(
            "jobLocation",
            {}
        )

        location = "Not Specified"

        if isinstance(
            location_data,
            dict
        ):

            address = location_data.get(
                "address",
                {}
            )

            if isinstance(
                address,
                dict
            ):

                city = address.get(
                    "addressLocality",
                    ""
                )

                region = address.get(
                    "addressRegion",
                    ""
                )

                country = address.get(
                    "addressCountry",
                    ""
                )

                location = ", ".join(
                    part
                    for part in [
                        city,
                        region,
                        country
                    ]
                    if part
                )

        elif isinstance(
            location_data,
            list
        ):

            locations = []

            for item in location_data:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                address = item.get(
                    "address",
                    {}
                )

                if isinstance(
                    address,
                    dict
                ):

                    city = address.get(
                        "addressLocality",
                        ""
                    )

                    country = address.get(
                        "addressCountry",
                        ""
                    )

                    value = ", ".join(
                        part
                        for part in [
                            city,
                            country
                        ]
                        if part
                    )

                    if value:
                        locations.append(
                            value
                        )

            if locations:

                location = " / ".join(
                    locations
                )

        description = BeautifulSoup(
            data.get(
                "description",
                ""
            ),
            "html.parser"
        ).get_text(
            " ",
            strip=True
        )

        salary = "Not Specified"

        salary_data = data.get(
            "baseSalary"
        )

        if isinstance(
            salary_data,
            dict
        ):

            value = salary_data.get(
                "value",
                {}
            )

            if isinstance(
                value,
                dict
            ):

                minimum = value.get(
                    "minValue"
                )

                maximum = value.get(
                    "maxValue"
                )

                currency = salary_data.get(
                    "currency",
                    ""
                )

                if minimum and maximum:

                    salary = (
                        f"{currency} "
                        f"{minimum} - "
                        f"{maximum}"
                    )

                elif minimum:

                    salary = (
                        f"{currency} "
                        f"{minimum}"
                    )

        return {
            "Job Title": title,
            "Company Name": company,
            "Location": location,
            "Experience": self.extract_experience(
                description
            ),
            "Skills": self.extract_skills(
                description
            ),
            "Salary": salary,
            "Source": "JSON-LD",
            "Job URL": data.get(
                "url",
                ""
            )
        }


    # ========================================================
    # SELECTOR SEARCH
    # ========================================================

    def find_from_selectors(
        self,
        element,
        selectors
    ):

        for selector in selectors:

            try:

                found = element.select_one(
                    selector
                )

                if found:

                    text = found.get_text(
                        " ",
                        strip=True
                    )

                    if text:

                        return text

            except Exception:

                continue

        return ""


    # ========================================================
    # EXPERIENCE
    # ========================================================

    def extract_experience(
        self,
        text
    ):

        patterns = [
            r"\d+\s*-\s*\d+\s*years?",
            r"\d+\+\s*years?",
            r"\d+\s*years?",
            r"\d+\s*-\s*\d+\s*yrs?"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group()

        return "Not Specified"


    # ========================================================
    # SALARY
    # ========================================================

    def extract_salary(
        self,
        text
    ):

        patterns = [
            r"₹\s?[\d,]+\s*[-–]\s*₹?\s?[\d,]+\s*(?:LPA|Lakh|Lakhs)?",
            r"₹\s?[\d,]+\s*(?:LPA|Lakh|Lakhs)",
            r"\$\s?[\d,]+\s*[-–]\s*\$?\s?[\d,]+",
            r"\$\s?[\d,]+\s*(?:USD|per year|/year)?",
            r"\d+\s*-\s*\d+\s*LPA"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group()

        return "Not Specified"


    # ========================================================
    # SKILLS
    # ========================================================

    def extract_skills(
        self,
        text
    ):

        found = []

        lower_text = text.lower()

        for skill in self.skills:

            if skill.lower() in lower_text:

                found.append(
                    skill
                )

        if found:

            return ", ".join(
                dict.fromkeys(
                    found
                )
            )

        return "Not Specified"


# ============================================================
# JOBSCOPE APPLICATION
# ============================================================

class JobScopeApp:

    def __init__(
        self,
        root
    ):

        self.root = root

        self.root.title(
            "JobScope | Job Market Intelligence"
        )

        self.root.geometry(
            "1400x880"
        )

        self.root.minsize(
            1100,
            700
        )

        self.root.configure(
            bg=BG
        )

        self.scraper = JobScraper()

        self.df = pd.DataFrame()

        self.current_view = "jobs"

        self.setup_styles()

        self.create_header()

        self.create_source_panel()

        self.create_dashboard()

        self.create_navigation()

        self.create_content()

        self.create_status()


    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        style.theme_use(
            "clam"
        )

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=TEXT,
            fieldbackground=PANEL,
            rowheight=34,
            borderwidth=0,
            font=(
                "Segoe UI",
                10
            )
        )

        style.configure(
            "Treeview.Heading",
            background=PURPLE_DARK,
            foreground=WHITE,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            padding=10
        )

        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    PURPLE
                )
            ],
            foreground=[
                (
                    "selected",
                    WHITE
                )
            ]
        )


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        frame = tk.Frame(
            self.root,
            bg=BG
        )

        frame.pack(
            fill="x",
            padx=35,
            pady=(25, 10)
        )

        tk.Label(
            frame,
            text="JOBSCOPE",
            bg=BG,
            fg=WHITE,
            font=(
                "Segoe UI",
                30,
                "bold"
            )
        ).pack(
            side="left"
        )

        tk.Label(
            frame,
            text="  JOB MARKET INTELLIGENCE",
            bg=BG,
            fg=CYAN,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            side="left",
            pady=(12, 0)
        )

        tk.Label(
            frame,
            text="SCRAPE  •  ANALYZE  •  DISCOVER",
            bg=BG,
            fg=MUTED,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            side="right",
            pady=12
        )


    # ========================================================
    # URL PANEL
    # ========================================================

    def create_source_panel(self):

        panel = tk.Frame(
            self.root,
            bg=PANEL
        )

        panel.pack(
            fill="x",
            padx=35,
            pady=10
        )

        tk.Label(
            panel,
            text="URL",
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            side="left",
            padx=(20, 10)
        )

        self.url_entry = tk.Entry(
            panel,
            bg=PANEL_2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=(
                "Segoe UI",
                11
            )
        )

        self.url_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            pady=15
        )

        self.url_entry.insert(
            0,
            "https://remotive.com/remote-jobs/o-python"
        )

        self.scrape_button = tk.Button(
            panel,
            text="SCAN URL",
            command=self.scan_url,
            bg=PURPLE,
            fg=WHITE,
            activebackground=PURPLE_DARK,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            padx=24,
            pady=11
        )

        self.scrape_button.pack(
            side="left",
            padx=10
        )

        demo_button = tk.Button(
            panel,
            text="DEMO DATA",
            command=self.load_demo_data,
            bg=PANEL_2,
            fg=CYAN,
            activebackground=PURPLE_DARK,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            padx=20,
            pady=11
        )

        demo_button.pack(
            side="left",
            padx=(0, 15)
        )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):

        frame = tk.Frame(
            self.root,
            bg=BG
        )

        frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.jobs_value = self.create_card(
            frame,
            "TOTAL JOBS",
            "0"
        )

        self.companies_value = self.create_card(
            frame,
            "COMPANIES",
            "0"
        )

        self.locations_value = self.create_card(
            frame,
            "LOCATIONS",
            "0"
        )

        self.roles_value = self.create_card(
            frame,
            "JOB ROLES",
            "0"
        )


    def create_card(
        self,
        parent,
        title,
        value
    ):

        card = tk.Frame(
            parent,
            bg=PANEL
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        tk.Label(
            card,
            text=title,
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 2)
        )

        value_label = tk.Label(
            card,
            text=value,
            bg=PANEL,
            fg=WHITE,
            font=(
                "Segoe UI",
                25,
                "bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 14)
        )

        return value_label


    # ========================================================
    # NAVIGATION
    # ========================================================

    def create_navigation(self):

        frame = tk.Frame(
            self.root,
            bg=BG
        )

        frame.pack(
            fill="x",
            padx=35,
            pady=(5, 8)
        )

        buttons = [
            ("ALL JOBS", self.show_jobs),
            ("JOB ROLES", self.show_roles),
            ("TOP SKILLS", self.show_skills),
            ("LOCATIONS", self.show_locations),
            ("SALARY", self.show_salary),
            ("LOAD CSV", self.load_csv),
            ("EXPORT CSV", self.export_csv)
        ]

        for text, command in buttons:

            tk.Button(
                frame,
                text=text,
                command=command,
                bg=PANEL,
                fg=TEXT,
                activebackground=PURPLE,
                activeforeground=WHITE,
                relief="flat",
                cursor="hand2",
                font=(
                    "Segoe UI",
                    9,
                    "bold"
                ),
                padx=14,
                pady=8
            ).pack(
                side="left",
                padx=(0, 7)
            )


    # ========================================================
    # CONTENT
    # ========================================================

    def create_content(self):

        container = tk.Frame(
            self.root,
            bg=PANEL
        )

        container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 8)
        )

        search_frame = tk.Frame(
            container,
            bg=PANEL
        )

        search_frame.pack(
            fill="x",
            padx=12,
            pady=(12, 5)
        )

        tk.Label(
            search_frame,
            text="SEARCH",
            bg=PANEL,
            fg=MUTED,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            side="left",
            padx=(5, 10)
        )

        self.search_entry = tk.Entry(
            search_frame,
            bg=PANEL_2,
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
            ipady=8
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_data
        )

        table_frame = tk.Frame(
            container,
            bg=PANEL
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=8
        )

        self.table = ttk.Treeview(
            table_frame,
            show="headings"
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        self.table.configure(
            yscrollcommand=scrollbar_y.set
        )


    # ========================================================
    # STATUS
    # ========================================================

    def create_status(self):

        self.status = tk.Label(
            self.root,
            text=(
                "Ready | Enter a job URL and click SCAN URL"
            ),
            bg=BG,
            fg=MUTED,
            anchor="w",
            font=(
                "Segoe UI",
                9
            )
        )

        self.status.pack(
            fill="x",
            padx=35,
            pady=(0, 10)
        )


    # ========================================================
    # SCAN URL
    # ========================================================

    def scan_url(self):

        url = (
            self.url_entry
            .get()
            .strip()
        )

        if not url.startswith(
            ("http://", "https://")
        ):

            messagebox.showwarning(
                "Invalid URL",
                "Enter a URL beginning with http:// or https://"
            )

            return

        self.scrape_button.config(
            state="disabled",
            text="SCANNING..."
        )

        self.status.config(
            text="Analyzing URL..."
        )

        self.root.update_idletasks()

        try:

            domain = urlparse(
                url
            ).netloc

            if "remotive.com" in domain:

                self.status.config(
                    text=(
                        "Detected Remotive → "
                        "using official public job API..."
                    )
                )

            else:

                self.status.config(
                    text=(
                        "Scanning HTML → "
                        "falling back to browser rendering if needed..."
                    )
                )

            self.root.update_idletasks()

            jobs = self.scraper.scan_url(
                url
            )

            self.df = pd.DataFrame(
                jobs
            )

            self.clean_data()

            self.save_data()

            self.update_dashboard()

            self.show_jobs()

            self.status.config(
                text=(
                    f"✓ Scan complete | "
                    f"{len(self.df)} jobs collected "
                    f"from {domain}"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "URL Scan Failed",
                str(error)
            )

            self.status.config(
                text="URL scan failed."

            )

        finally:

            self.scrape_button.config(
                state="normal",
                text="SCAN URL"
            )


    # ========================================================
    # CLEAN DATA
    # ========================================================

    def clean_data(self):

        if self.df.empty:

            return

        self.df = (
            self.df
            .drop_duplicates()
            .reset_index(drop=True)
        )

        for column in self.df.columns:

            self.df[column] = (
                self.df[column]
                .fillna("Not Specified")
                .astype(str)
                .str.strip()
            )


    # ========================================================
    # SAVE
    # ========================================================

    def save_data(self):

        try:

            os.makedirs(
                "data",
                exist_ok=True
            )

            self.df.to_csv(
                "data/jobs.csv",
                index=False
            )

        except Exception:

            pass


    # ========================================================
    # UPDATE DASHBOARD
    # ========================================================

    def update_dashboard(self):

        if self.df.empty:

            return

        self.jobs_value.config(
            text=len(self.df)
        )

        self.companies_value.config(
            text=self.df[
                "Company Name"
            ].nunique()
        )

        self.locations_value.config(
            text=self.df[
                "Location"
            ].nunique()
        )

        self.roles_value.config(
            text=self.df[
                "Job Title"
            ].nunique()
        )


    # ========================================================
    # DISPLAY TABLE
    # ========================================================

    def display_data(
        self,
        dataframe
    ):

        for item in self.table.get_children():

            self.table.delete(
                item
            )

        if dataframe.empty:

            return

        columns = list(
            dataframe.columns
        )

        self.table["columns"] = columns

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=180,
                anchor="w"
            )

        for _, row in dataframe.iterrows():

            values = [
                str(value)
                for value in row
            ]

            self.table.insert(
                "",
                "end",
                values=values
            )


    # ========================================================
    # ALL JOBS
    # ========================================================

    def show_jobs(self):

        if self.df.empty:

            messagebox.showinfo(
                "No Data",
                "Load data first."
            )

            return

        self.current_view = "jobs"

        self.display_data(
            self.df
        )

        self.status.config(
            text=(
                f"Showing {len(self.df)} jobs"
            )
        )


    # ========================================================
    # SEARCH
    # ========================================================

    def search_data(
        self,
        event=None
    ):

        if self.df.empty:

            return

        keyword = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if not keyword:

            self.show_jobs()

            return

        mask = (
            self.df
            .astype(str)
            .apply(
                lambda column:
                column.str.lower().str.contains(
                    keyword,
                    na=False
                )
            )
            .any(axis=1)
        )

        filtered = self.df[
            mask
        ]

        self.display_data(
            filtered
        )

        self.status.config(
            text=(
                f"Search results: "
                f"{len(filtered)} jobs"
            )
        )


    # ========================================================
    # ROLES
    # ========================================================

    def show_roles(self):

        if self.df.empty:

            messagebox.showinfo(
                "No Data",
                "Load data first."
            )

            return

        self.current_view = "roles"

        data = (
            self.df[
                "Job Title"
            ]
            .value_counts()
            .head(15)
        )

        result = data.reset_index()

        result.columns = [
            "Job Title",
            "Number of Jobs"
        ]

        self.display_data(
            result
        )

        self.status.config(
            text="Most common job roles"
        )

        self.create_chart(
            data,
            "Most Common Job Roles",
            "Job Role",
            "Job Listings"
        )


    # ========================================================
    # SKILLS
    # ========================================================

    def show_skills(self):

        if self.df.empty:

            messagebox.showinfo(
                "No Data",
                "Load data first."
            )

            return

        self.current_view = "skills"

        counter = {}

        for skills in self.df[
            "Skills"
        ]:

            if skills == "Not Specified":

                continue

            for skill in skills.split(","):

                skill = skill.strip()

                if skill:

                    counter[skill] = (
                        counter.get(
                            skill,
                            0
                        ) + 1
                    )

        data = pd.Series(
            counter
        ).sort_values(
            ascending=False
        ).head(15)

        result = data.reset_index()

        result.columns = [
            "Skill",
            "Demand"
        ]

        self.display_data(
            result
        )

        self.status.config(
            text="Most demanded skills"
        )

        self.create_chart(
            data,
            "Most Demanded Skills",
            "Skill",
            "Job Listings"
        )


    # ========================================================
    # LOCATIONS
    # ========================================================

    def show_locations(self):

        if self.df.empty:

            messagebox.showinfo(
                "No Data",
                "Load data first."
            )

            return

        self.current_view = "locations"

        data = (
            self.df[
                "Location"
            ]
            .value_counts()
            .head(15)
        )

        result = data.reset_index()

        result.columns = [
            "Location",
            "Number of Jobs"
        ]

        self.display_data(
            result
        )

        self.status.config(
            text="Top job locations"
        )

        self.create_chart(
            data,
            "Top Job Locations",
            "Location",
            "Job Listings"
        )


    # ========================================================
    # SALARY
    # ========================================================

    def show_salary(self):

        if self.df.empty:

            messagebox.showinfo(
                "No Data",
                "Load data first."
            )

            return

        self.current_view = "salary"

        result = self.df[
            [
                "Job Title",
                "Company Name",
                "Location",
                "Salary"
            ]
        ]

        self.display_data(
            result
        )

        self.status.config(
            text="Salary information"
        )


    # ========================================================
    # CHART
    # ========================================================

    def create_chart(
        self,
        data,
        title,
        xlabel,
        ylabel
    ):

        if data.empty:

            return

        os.makedirs(
            "charts",
            exist_ok=True
        )

        plt.close(
            "all"
        )

        plt.figure(
            figsize=(11, 6)
        )

        data.plot(
            kind="bar"
        )

        plt.title(
            title,
            fontsize=16,
            fontweight="bold"
        )

        plt.xlabel(
            xlabel
        )

        plt.ylabel(
            ylabel
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        try:

            plt.savefig(
                "charts/latest_chart.png",
                dpi=150
            )

        except Exception:

            pass

        plt.show()


    # ========================================================
    # LOAD CSV
    # ========================================================

    def load_csv(self):

        path = filedialog.askopenfilename(
            title="Select Job CSV",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                )
            ]
        )

        if not path:

            return

        try:

            dataframe = pd.read_csv(
                path
            )

            required_columns = [
                "Job Title",
                "Company Name",
                "Location",
                "Experience",
                "Skills",
                "Salary"
            ]

            missing = [
                column
                for column in required_columns
                if column not in dataframe.columns
            ]

            if missing:

                messagebox.showerror(
                    "Invalid CSV",
                    (
                        "Missing columns:\n\n"
                        + "\n".join(
                            missing
                        )
                    )
                )

                return

            self.df = dataframe[
                required_columns
            ].copy()

            self.clean_data()

            self.save_data()

            self.update_dashboard()

            self.show_jobs()

            self.status.config(
                text=(
                    f"CSV loaded successfully | "
                    f"{len(self.df)} jobs"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "CSV Error",
                str(error)
            )


    # ========================================================
    # EXPORT CSV
    # ========================================================

    def export_csv(self):

        if self.df.empty:

            messagebox.showinfo(
                "No Data",
                "Load data first."
            )

            return

        path = filedialog.asksaveasfilename(
            title="Export Job Dataset",
            defaultextension=".csv",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                )
            ]
        )

        if not path:

            return

        try:

            self.df.to_csv(
                path,
                index=False
            )

            messagebox.showinfo(
                "Export Complete",
                "Job dataset exported successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


    # ========================================================
    # DEMO DATA
    # ========================================================

    def load_demo_data(self):

        self.df = pd.DataFrame({

            "Job Title": [
                "Python Developer",
                "Data Scientist",
                "Machine Learning Engineer",
                "Python Developer",
                "Data Analyst",
                "AI Engineer",
                "Software Engineer",
                "Data Scientist",
                "ML Engineer",
                "AI Engineer",
                "Data Analyst",
                "Python Developer",
                "Data Engineer",
                "AI Developer",
                "Software Engineer",
                "Cloud Engineer",
                "Data Scientist",
                "Python Developer",
                "ML Engineer",
                "Data Analyst"
            ],

            "Company Name": [
                "TechNova",
                "DataSphere",
                "AI Labs",
                "CloudWorks",
                "Insight Analytics",
                "FutureAI",
                "CodeCraft",
                "DataSphere",
                "AI Labs",
                "FutureAI",
                "Insight Analytics",
                "TechNova",
                "CloudWorks",
                "FutureAI",
                "CodeCraft",
                "CloudWorks",
                "DataSphere",
                "TechNova",
                "AI Labs",
                "Insight Analytics"
            ],

            "Location": [
                "Chennai",
                "Bangalore",
                "Hyderabad",
                "Chennai",
                "Bangalore",
                "Remote",
                "Pune",
                "Bangalore",
                "Hyderabad",
                "Remote",
                "Chennai",
                "Pune",
                "Bangalore",
                "Chennai",
                "Hyderabad",
                "Bangalore",
                "Remote",
                "Chennai",
                "Hyderabad",
                "Pune"
            ],

            "Experience": [
                "0-2 years",
                "1-3 years",
                "2-4 years",
                "0-2 years",
                "1-2 years",
                "2-4 years",
                "1-3 years",
                "1-3 years",
                "2-4 years",
                "2-5 years",
                "0-2 years",
                "0-2 years",
                "1-3 years",
                "1-3 years",
                "1-3 years",
                "2-4 years",
                "1-3 years",
                "0-2 years",
                "2-4 years",
                "1-2 years"
            ],

            "Skills": [
                "Python, SQL, Git",
                "Python, SQL, Machine Learning",
                "Python, TensorFlow, Docker",
                "Python, Django, SQL",
                "SQL, Power BI, Excel",
                "Python, Deep Learning, AWS",
                "Java, Spring, SQL",
                "Python, Machine Learning, SQL",
                "Python, PyTorch, Docker",
                "Python, NLP, AWS",
                "SQL, Excel, Power BI",
                "Python, Git, MongoDB",
                "Python, SQL, AWS",
                "Python, Artificial Intelligence, NLP",
                "Java, SQL, Git",
                "AWS, Docker, Python",
                "Python, Machine Learning, SQL",
                "Python, Django, Git",
                "Python, PyTorch, Machine Learning",
                "SQL, Excel, Power BI"
            ],

            "Salary": [
                "₹6-10 LPA",
                "₹8-14 LPA",
                "₹10-18 LPA",
                "₹5-9 LPA",
                "₹5-8 LPA",
                "₹10-18 LPA",
                "₹6-11 LPA",
                "₹8-14 LPA",
                "₹10-17 LPA",
                "₹9-16 LPA",
                "₹5-9 LPA",
                "₹6-10 LPA",
                "₹7-13 LPA",
                "₹8-15 LPA",
                "₹6-11 LPA",
                "₹8-15 LPA",
                "₹9-15 LPA",
                "₹6-10 LPA",
                "₹10-17 LPA",
                "₹5-9 LPA"
            ]
        })

        self.df["Source"] = "Demo"

        self.df["Job URL"] = "Demo"

        self.clean_data()

        self.save_data()

        self.update_dashboard()

        self.show_jobs()

        self.status.config(
            text=(
                "Demo data loaded | "
                f"{len(self.df)} jobs"
            )
        )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    JobScopeApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()
