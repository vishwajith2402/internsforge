# JobScope – Job Market Intelligence

## Project Objective

JobScope is a Python-based web scraping and job market analysis application.

The system collects job listing information such as:

- Job Title
- Company Name
- Location
- Experience
- Skills
- Salary

The collected information is cleaned, stored in CSV format and analyzed to identify job market trends.

---

## Problem Statement

Job seekers often find it difficult to understand which roles, locations and technical skills are currently demanded by employers.

JobScope addresses this problem by collecting job listing data and converting it into useful insights.

---

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- Tkinter
- CSV

---

## Features

### Web Scraping

Scrapes job listing information from supported websites.

### Data Cleaning

Removes duplicate records and handles missing values.

### Job Role Analysis

Identifies the most frequently occurring job roles.

### Skill Analysis

Finds the most demanded technical skills.

### Location Analysis

Identifies locations with the highest number of job listings.

### CSV Export

Allows users to export collected job data.

### Dashboard

Displays:

- Total Jobs
- Companies
- Locations
- Job Roles

---

## Dataset Columns

| Column | Description |
|---|---|
| Job Title | Name of the job |
| Company Name | Hiring company |
| Location | Job location |
| Experience | Required experience |
| Skills | Required skills |
| Salary | Salary information |

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt