# Tour Booking Platform  

A web application for booking and managing travel packages with multi-agency support.  

---

## 🚀 Features

- User registration, login, and profile management  
- Search & filter tour packages by destination, price, or availability  
- Booking system with confirmation  
- Travel agency dashboard to add and manage packages  
- Admin panel to monitor users, agencies, and bookings  
- Secure authentication & authorization (role-based)  
- Database-driven storage of packages, users, and bookings  

---

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Frontend:** HTML, CSS, JavaScript  
- **Deployment:** Docker, Render / NxtGen (hosting platform)  
- **Tools:** Git, GitHub, VS Code  

---

## 📦 Installation & Setup  

1. Clone the repository:  
   ```bash
   git clone https://github.com/varsha20092000/Tour-project-clean.git
   cd Tour-project-clean
2. Create virtual environment & install dependencies:
     pip install -r requirements.txt
3. Set up environment variables in .env:
      DEBUG=True
      DATABASE_URL=postgres://user:pass@localhost:5432/tourdb
      SECRET_KEY=your_secret_key

4. Run migrations:
      python manage.py migrate

5. Start development server:
     python manage.py runserver

✅ Testing:
      python manage.py test


