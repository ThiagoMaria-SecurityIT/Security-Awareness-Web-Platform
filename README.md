# Security Awareness Web Platform

A Python Flask web application for security awareness training that uses LibreOffice to convert PowerPoint presentations into course slides and SQLAlchemy for database management.

This platform is designed to help organizations manage their annual security awareness training programs, a common requirement for compliance with frameworks like **ISO 27001, NIST, SOC 2, and PCI-DSS**.

## Table of Contents

1.  [The Problem This Solves](#the-problem-this-solves)
2.  [Core Features](#core-features)
3.  [How to Run This Project](#how-to-run-this-project)
4.  [Troubleshooting](#troubleshooting)
5.  [Future Implementations](#future-implementations)
6.  [AI Transparency](#ai-transparency)
7.  [About Me & Contact](#about-me--contact)
8.  [Ways to Contribute](#ways-to-contribute)

## The Problem This Solves

Many organizations struggle with efficiently managing and tracking their mandatory annual security awareness training. This project solves several key problems:

*   **User Management:** Instead of manually tracking users in spreadsheets, this platform provides a central database to manage all employees, their roles, and their training status.
*   **Course Assignment:** Easily assign specific training courses to individuals or entire teams, ensuring everyone receives the required training.
*   **Completion Tracking:** The platform provides a clear overview of who has completed their assigned training and who has not, which is crucial for audit and compliance purposes.
*   **Content Flexibility:** Use your existing PowerPoint (`.pptx`) training materials. The platform automatically converts them into a web-based course, saving time and resources.

## Core Features

*   **Role-Based Access:** Different views and permissions for Learners, Trainers, and Admins.
*   **Automated Course Conversion:** Upload a `.pptx` file, and it becomes an interactive web course.
*   **Course Management Hub:** A central dashboard for trainers to upload, view, list, and delete courses.
*   **User & Enrollment Database:** Tracks all users and their course enrollment history.

## How to Run This Project

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/ThiagoMaria-SecurityIT/Security-Awareness-Web-Platform.git
    cd Security-Awareness-Web-Platform
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install LibreOffice:**
    This is required for the automatic conversion of PowerPoint files.
    *   Download from [libreoffice.org](https://www.libreoffice.org/download/download-libreoffice/).
    *   Ensure the path to LibreOffice in `app.py` is correct for your system.

5.  **Run the Application:**
    ```bash
    python app.py
    ```
    The app will start, create the necessary folders and database, and be accessible at `http://127.0.0.1:5000`.

6.  **Default Admin Login:**
    *   **Email:** `superadmin@app.com`
    *   **Password:** `superadmin123`

## Troubleshooting

If the application crashes or you get an error because your session is stuck, you may need to manually log out. Simply navigate to the logout URL in your browser:
[http://127.0.0.1:5000/logout](http://127.0.0.1:5000/logout)

This will clear your session and redirect you to the login page.

## Future Implementations

The roadmap for this project includes several exciting features:

*   **Certificate Generation:** Automatically generate a PDF certificate upon course completion.
*   **Bulk User Management:** Import and export user lists from a `.csv` file.
*   **Advanced Reporting:** Detailed dashboards for compliance and audit reports.

## AI Transparency

This project was developed with the significant use of an AI assistant, **Manus**, for code generation, debugging, and architectural guidance. The process was collaborative, where the logic and feature requests were directed by a human developer who also reviewed, tested, and refined the AI-generated code to ensure it met the project's goals and quality standards. This project is a testament to human-AI partnership in modern software development.

## About Me & Contact

**Thiago Maria - From Brazil to the World 🌎**  
*Senior Security Information Professional | Passionate Programmer | AI Developer*

My passion for programming and my professional background in security analysis led me to create this GitHub account to share my knowledge of security information, cybersecurity, Python, and AI development practices. My work primarily focuses on prioritizing security in organizations while ensuring usability and productivity.

Let's Connect:  

👇🏽 Click on the badges below:  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/thiago-cequeira-99202239/)  
[![Hugging Face](https://img.shields.io/badge/🤗Hugging_Face-AI_projects-yellow)](https://huggingface.co/ThiSecur)  
 
## Ways to Contribute
Want to see more upgrades? Help me keep it updated!    
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://github.com/sponsors/ThiagoMaria-SecurityIT)
