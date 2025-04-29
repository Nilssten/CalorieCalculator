# 🥗 Calorie Calculator (Flask + Docker)

A bilingual (Latvian/English) calorie calculator web app built with Flask, HTML, CSS, and Docker.

---

## 🚀 How to Run This App Using Docker

### 🐳 Prerequisites

- Docker Desktop installed on your machine.
- Git installed (optional, if cloning directly from GitHub).

---

### 📦 Option 1: Clone and Run From GitHub

```bash
git clone https://github.com/Nilssten/CalorieCalculator.git
cd CalorieCalculator
docker build -t calorie-calculator .
docker run -d -p 5000:80 calorie-calculator
```

### 📁 Option 2: If You Have a ZIP File
1.	Extract the CalorieCalculator.zip
2.	Open Terminal in the extracted folder.
3.	Run the following:
```bash
docker build -t calorie-calculator .
docker run -d -p 5000:80 calorie-calculator
```
---
### 🛠️ Notes
- 	If port 5000 is in use, replace it with another, e.g.:
```bash
docker run -d -p 5001:80 calorie-calculator
```
- 	This app runs on Flask’s development server. For production, use a proper WSGI server like Gunicorn.
### 🌐 Languages Supported
- 🇱🇻 Latvian
- 🇬🇧 English
 
