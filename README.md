# ✅ To-Do List Web App

A full-stack, user-authenticated to-do list web application built with **Flask**, **Firebase Authentication**, and **PostgreSQL**. 
Users can log in, manage personal tasks, and track completion status — all from a responsive interface deployed to the cloud via **Render**.

---

## 🚀 Live Demo

🌐 [https://todo-list-app-rp29.onrender.com](https://todo-list-app-rp29.onrender.com)  


---

## 🔐 Features

- **User Authentication** with Firebase (Email/Password)
- **Per-user task storage** using PostgreSQL linked to Firebase UID
- Add, edit, delete, and mark tasks as complete/incomplete
- Task counters for completed and pending items
- Fully deployed using Render

---

## 🧰 Tech Stack

| Layer      | Tool                            |
|------------|---------------------------------|
| Backend    | Flask (Python)                  |
| Frontend   | HTML, CSS, JavaScript           |
| Auth       | Firebase Authentication         |
| Database   | PostgreSQL (hosted on Render)   |
| Hosting    | Render.com                      |

---

## 📁 Project Structure
Todo-List-App/
├── static/
│ ├── login.js
│ ├── signup.js
│ └── todo.js
├── templates/
│ ├── index.html
│ ├── login.html
│ └── signup.html
├── app.py
├── requirements.txt
└── README.md
