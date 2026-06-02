# Multi-Tool Django Automation Platform

A modular Django platform that integrates multiple automation tools into a single application. It combines email automation with open/click tracking, async CSV data import/export, image compression, and real-time stock web scraping — all powered by **Celery** and **Redis** for background task processing.

---

## Modules

### 📧 Email Automation
- Send bulk emails to subscriber lists with **rich text (CKEditor)** body and optional file attachments
- Background email delivery via **Celery** — non-blocking, queue-based
- **Email open tracking** — invisible 1×1 pixel injected into each email
- **Email click tracking** — links in email body are replaced with tracking URLs before sending
- Each subscriber gets a unique SHA-256 tracking ID per email
- Analytics dashboard showing open rate and click rate per email
- Per-email stats page with total sent count

### 📂 CSV Data Import / Export
- Upload a CSV file and select any custom model to import data into
- CSV headers are validated against model fields before import begins
- Import runs as a **Celery background task** — user is notified by email on completion
- Export any model's data to CSV as a **Celery background task** — exported file is emailed as an attachment
- Custom Django management commands: `importdata`, `exportdata`, `insertdata`, `greeting`, `helloworld`

### 🖼️ Image Compression
- Upload any image and select a quality level (10–100)
- Image is compressed using **Pillow** and auto-converted to JPEG if needed
- Compressed file is returned as a direct download response

### 📈 Stock Web Scraping
- Search for a stock by name or symbol with **autocomplete** (django-autocomplete-light / Select2)
- Scrapes real-time stock data (current price, price change, percentage change) using **BeautifulSoup**
- Saves scraped results to the database per query

---

## Tech Stack

- **Backend:** Python, Django 6
- **Task Queue:** Celery 5, Redis
- **Web Scraping:** BeautifulSoup4, Requests
- **Image Processing:** Pillow
- **Email:** Django EmailMessage (SMTP), django-anymail
- **Rich Text:** django-ckeditor
- **Autocomplete:** django-autocomplete-light (Select2)
- **Forms:** django-crispy-forms, crispy-bootstrap5
- **Database:** SQLite
- **Config:** python-decouple

---

## Project Structure

```
Automate_django/
├── awd_main/           # Django project settings, root URLs, celery config, auth views
├── emails/             # Email lists, subscribers, bulk sending, open/click tracking
├── dataentry/          # CSV import/export, management commands, Celery tasks
├── image_compress/     # Image upload and compression
├── stockanalysis/      # Stock model, web scraping, autocomplete
├── uploads/            # File upload model (used by dataentry)
├── templates/          # All HTML templates
│   ├── emails/
│   ├── dataentry/
│   ├── image_compress/
│   └── stockanalysis/
├── stocks.py           # Web scraping logic (BeautifulSoup)
├── manage.py
└── requirements.txt
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/SherazHaider907/Automate_django.git
cd Automate_django
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:
```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DEFAULT_FROM_EMAIL=your_email@gmail.com
DEFAULT_TO_EMAIL=recipient@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Start Redis (required for Celery)

Make sure Redis is running locally:
```bash
# Windows (via WSL or Docker)
docker run -d -p 6379:6379 redis

# Mac/Linux
redis-server
```

### 8. Start the Celery worker (in a separate terminal)
```bash
celery -A awd_main worker --loglevel=info
```

### 9. Run the Django server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/emails/send/` | Send bulk email to a subscriber list |
| `/emails/track/dashboard/` | Email analytics dashboard |
| `/emails/track/stats/<id>/` | Per-email stats (open rate, click rate) |
| `/dataentry/import/` | Import CSV data into any model |
| `/dataentry/export/` | Export any model's data to CSV |
| `/image_compress/` | Upload and compress an image |
| `/webscrapping/` | Search and scrape real-time stock data |
| `/register/` | User registration |
| `/login/` | User login |
| `/admin/` | Django admin panel |
| `/celery-test/` | Trigger a test Celery task |
