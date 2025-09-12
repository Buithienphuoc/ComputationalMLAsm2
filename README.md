# AI Predictor SPA (Django Project)

This project is a Django-based Single Page Application (SPA) for predicting goal accuracy in Premier League 2025 using AI/ML models.  
It includes authentication, prediction, and history tracking features.

---

## 🚀 Features
- User authentication (login/logout)
- AI model prediction for player shot accuracy
- History of predictions (latest 50 records)
- Admin panel for managing users and data
- Dark/Light mode toggle UI
- Bootstrap-based responsive interface

---

## 📂 Project Structure
```
project_root/
│── ai_app/              # Main Django app
│    └── static/ai_app/  # Static files (CSS, JS, images, logo)
│── templates/           # HTML templates
│── manage.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone repository
```bash
git clone <your-repo-url>
cd project_root
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create superuser (for Django admin)
```bash
python manage.py createsuperuser
```

### 6. Run development server
```bash
python manage.py runserver
```

Now open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Admin Panel
Visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)  
Login with your superuser credentials.

---

## 🎨 Static Files
- Place CSS/JS/images in:  
  ```
  ai_app/static/ai_app/
  ```
- Example usage in template:
  ```html
  {% load static %}
  <img src="{% static 'ai_app/pictures/trollface_35x35.jpg' %}" alt="Logo">
  ```

---

## 🌍 Deployment Notes
- For production, set:
  ```python
  DEBUG = False
  ALLOWED_HOSTS = ['*']  # or your domain
  ```
- Collect static files:
  ```bash
  python manage.py collectstatic
  ```
- Configure web server (Gunicorn, Nginx, or use services like PythonAnywhere / AWS).

---

## ✅ Quick Demo Credentials
Demo user will be created automatically:
```
Username: user
Password: 123456
```
