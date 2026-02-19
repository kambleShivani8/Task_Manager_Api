# 📝 Task Manager API

A production-ready Task Manager REST API built using **FastAPI**, **SQLAlchemy**, and **JWT Authentication**.

This project allows users to register, login, and manage their tasks securely.

🚀 Deployed on Render.

---

## 🌐 Live Deployment

🔗 https://your-render-url.onrender.com  
🔗 https://your-render-url.onrender.com/docs

---

## 🛠 Tech Stack

- **FastAPI** – Modern Python web framework
- **SQLAlchemy** – ORM for database operations
- **SQLite** – Lightweight database
- **Pydantic** – Data validation and schemas
- **python-jose** – JWT authentication
- **Passlib (bcrypt)** – Secure password hashing
- **Uvicorn** – ASGI server
- **Render** – Cloud deployment platform

---

## 🔐 Features

- User Registration
- User Login (JWT Authentication)
- Create Task
- Update Task
- Delete Task
- View All Tasks
- Protected Routes using JWT
- Automatic API Documentation (Swagger)

---
📂 Project Structure

Task_Manager_Api/
│
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models/
│ ├── schemas/
│ ├── routers/
│ └── auth/
│
├── requirements.txt
└── README.md


---

## ⚙️ How To Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Task_Manager_Api.git
cd Task_Manager_Api


## 📂 Project Structure

1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Task_Manager_Api.git
cd Task_Manager_Api
2️⃣ Create Virtual Environment
python -m venv venv
3️⃣ Activate Virtual Environment
Windows:

venv\Scripts\activate
4️⃣ Install Dependencies
pip install -r requirements.txt
5️⃣ Run Application
If main.py is inside app/ folder:

uvicorn app.main:app --reload
6️⃣ Open in Browser
Main URL:

http://127.0.0.1:8000
Swagger Documentation:

http://127.0.0.1:8000/docs
☁️ How To Deploy On Render
Push code to GitHub

Login to Render

Create New Web Service

Connect GitHub repository

### Build Command:
pip install -r requirements.txt
Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
⚠️ Use $PORT (important for Render)

🎯 Project Highlights
Built scalable REST API using FastAPI

Implemented JWT-based authentication

Used SQLAlchemy ORM for clean database handling

Fixed deployment errors and configured production environment

Successfully deployed to cloud platform (Render)

# ✅ Now Commit It

After saving:



git add README.md
git commit -m "Added complete project README"
git push origin main

