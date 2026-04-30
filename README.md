# ⚙️ Python Automation & Data Engineering Portfolio

**Gaurav Avhad** | Python Automation Engineer
[LinkedIn](https://www.linkedin.com/in/gauravavhad-python) | Mumbai, India

Welcome to my technical portfolio. This repository contains industrial-grade Python automation scripts and data pipelines designed to eliminate manual workflows, enhance system monitoring, and securely manage enterprise data.

---

## 🚀 Featured Projects

### 1. E-Commerce Price Intelligence & ETL Pipeline

An end-to-end Extract, Transform, Load (ETL) data pipeline that tracks competitor pricing in real-time, stores it securely, and generates automated visual reports.

- **Tech Stack:** Python 3.12, BeautifulSoup4, SQLite, Matplotlib, Requests
- **Architecture & Features:**
  - **Extract:** Bypasses anti-bot mechanisms using dynamic User-Agent rotation.
  - **Transform:** Cleans raw HTML string data, resolving UTF-8 encoding artifacts and casting strings to mathematical floats.
  - **Load:** Stores structured data into a relational **SQLite database** using parameterized queries to prevent SQL injection.
  - **Visualize:** Generates automated, dynamic bar charts using **Matplotlib** for rapid market analysis.

![Market Analysis Chart](chart.png)

### 2. AI-Powered Log Auditor & REST API

An automated log parsing system that utilizes advanced Regex to detect system failures and leverages GenAI to perform Root Cause Analysis (RCA). Evolved from a local CLI script into a fully functional web service.

- **Tech Stack:** Python 3.12, FastAPI, Pydantic, Google Gemini GenAI API, Regex
- **Architecture & Features:**
  - **Version 1 (CLI):** Processes local `.log` files and generates structured CSV reports for batch analysis.
  - **Version 2 (REST API):** An enterprise-grade endpoint (`/api/v1/audit-log`) built with **FastAPI**. It securely accepts raw server logs via POST requests, validates the payload, and instantly returns AI-categorized JSON error reports for downstream monitoring dashboards.

### 3. SecureVault - Encrypted Password Management

A secure Command Line Interface (CLI) credential manager implementing AES-256 symmetric encryption.

- **Tech Stack:** Python 3.12, Cryptography (Fernet), File I/O
- **Architecture & Features:**
  - Utilizes zero-knowledge architecture and secure file I/O to ensure credentials are never exposed in plain text.
  - Implements full CRUD (Create, Read, Update, Delete) operations with robust error handling for a seamless terminal user experience.

---

## 🛠️ Technical Capabilities

- **Core:** Python 3.12, SQL, Java
- **Backend & APIs:** FastAPI, RESTful API Development, Pydantic, JSON
- **Data Engineering:** ETL Pipelines, Relational Databases (SQLite), Web Scraping (BeautifulSoup4), Data Visualization (Matplotlib)
- **Automation & Ops:** Regex Log Parsing, File I/O, Automated Workflows, Splunk/AWS CloudWatch concepts
- **Security:** AES-256 Encryption, Parameterized SQL Queries, Secure API Integration
