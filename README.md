# 🚀 Multi-Tool Django Platform

This project is a modular Django-based system that integrates multiple tools into a single platform.

---

## 🧰 Features / Tools

### 📥 Data Import Tool
- Upload CSV files
- Store data into database

### 📤 Data Export Tool
- Export database records as CSV files

### 📧 Bulk Email System
- Send emails to multiple users
- Supports templates and attachments

### 📊 Email Tracking System
- Track email opens and clicks
- View analytics dashboard

### 🖼️ Image Compression Tool
- Upload and compress images using Pillow
- Store optimized images

### 🌐 Web Scraping Tool
- Extract stock data from external sources

---

## ⚙️ Tech Stack

- Django
- Celery
- Redis
- BeautifulSoup
- Requests
- Pillow
- Bootstrap

---

## 📦 Installation

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
