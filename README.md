 Spendo — Voice-Enabled Expense Tracker

Spendo is a smart, voice-enabled expense tracker that allows users to log and view expenses using natural speech. It’s designed to simplify personal finance tracking with a minimal, intuitive interface and smart backend features.

---

 Features

- Voice input for adding expenses
- Expense visualization and summary
- User authentication (Google OAuth)
- Secrets managed securely via `.env`
- Clean and modular Django structure

---

 Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Django + Python
- Database: SQLite3 (local)
- Voice Recognition: Web Speech API / `speech_recognition`
- Authentication: Google OAuth 2.0

---

 Setup Instructions

 1. Clone the repo

```bash
git clone https://github.com/AmulyaCswamy23/Spendo.git
cd Spendo
2. create a virtual environment
python -m venv venv
venv\Scripts\activate  # on Windows
# or
source venv/bin/activate  # on macOS/Linux
3.Install dependencies
pip install -r requirements.txt
4.Set up env file
SECRET_KEY=your-django-secret-key
DEBUG=True
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
5.Apply migrations
python manage.py migrate
6.Run the server
python manage.py runserver



FOLDER STRUCTURE
Spendo/
├── spendo/               # Django project settings
│   ├── settings.py
├── tracker/              # Expense tracking app
│   ├── views.py
├── templates/
├── static/
├── db.sqlite3            # (gitignored)
├── .env                  # (not pushed)
├── .gitignore
└── manage.py
