# Security Awareness Web Platform

<p align="center">
  <img src="https://img.shields.io/badge/status-under%20development-yellow" alt="Status: Under Development"/>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python Version"/>
  <img src="https://img.shields.io/badge/framework-Flask-black" alt="Framework: Flask"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License: MIT"/>
</p>

A Python Flask web application for security awareness training that uses LibreOffice to convert PowerPoint presentations into course slides and SQLAlchemy for database management.

This platform is designed to help organizations manage their annual security awareness training programs, a common requirement for compliance with frameworks like **ISO 27001, NIST, SOC 2, and PCI-DSS**.

> [!Tip]
> To see how this project started, check out the original desktop version built with Tkinter!  
> You can find it here: **[Security-Awareness-APP](https://github.com/ThiagoMaria-SecurityIT/Security-Awareness-APP )**  

<p align="center">
  <img width="100%" alt="Main dashboard of the Security Awareness Web Platform" src="https://github.com/user-attachments/assets/9482afd1-d6b7-426b-96fe-8b12468cafc5" />
</p>

## Table of Contents

1.  [The Problem This Solves](#the-problem-this-solves)
2.  [Core Features](#core-features)
3.  [Development Roadmap](#development-roadmap)
4.  [How to Run This Project](#how-to-run-this-project)
5.  [Troubleshooting](#troubleshooting)
6.  [Application Screenshots](#application-screenshots)
7.  [AI Transparency](#ai-transparency)
8.  [About Me & Contact](#about-me--contact)
9.  [Ways to Contribute](#ways-to-contribute)

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

## Development Roadmap

This project is currently under active development. Key features like the interactive course viewer and course completion logic are still being implemented.

The goal is to have these features fully functional by **December 2025**. The implementation will be based on the logic from the previous Tkinter version of this application (which already has a working presentation preview) and will be expanded upon as development time allows.

You can find the original Tkinter version here for reference:
[https://github.com/ThiagoMaria-SecurityIT/Security-Awareness-APP](https://github.com/ThiagoMaria-SecurityIT/Security-Awareness-APP)

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

## Application Screenshots

| Manage Courses | Assign Course |
| :---: | :---: |
| <img width="100%" alt="Assign Course page" src="https://github.com/user-attachments/assets/6583d02a-3013-4c82-868d-8d97cf81bc60" />  | <img width="100%" alt="Team Progress page" src="https://github.com/user-attachments/assets/0c50d2ea-3334-4d14-8d9d-a3e8b6dd8c90" /> |
| **Team Progress** | **User Management** |
|  <img width="100%" alt="User Management page" src="https://github.com/user-attachments/assets/f7eb7dbc-7f88-4438-b79f-5e2fbf6b3c2b" /> | <img width="100%" alt="Login page" src="https://github.com/user-attachments/assets/7dc90b89-383d-47cf-ba7c-d2997733e703" />|
| **Login Page** |  **Dashboard** |
| <img width="1914" height="827" alt="image" src="https://github.com/user-attachments/assets/0fdfdcec-e0e5-4054-a718-d4e489149307" /> | <img width="100%" alt="Manage Courses page" src="https://github.com/user-attachments/assets/7c0c2a65-923c-4940-b40a-44c4172ff192" /> |

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
