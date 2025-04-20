# 💰 Money Tracker - Flask API + VUE

A simple RESTful API built using **Flask** and **VUE** to manage and categorize personal financial transactions. This project is designed to help users track their income and expenses in categorized groups (A–E), with full CRUD operations.

---

## ⚙️ Features

- Add new transactions with name, date, description, category, and amount.
- Retrieve all transactions grouped by category (A–E).
- Edit and delete specific transactions.
- Simple login endpoint with hardcoded credentials.
- MySQL backend integration with SQLAlchemy ORM.
- CORS enabled for all routes.

---
## 🛠️ Prerequisites

Ensure the following are installed on your system:

- **Python 3**
- **flask, flask_sqlalchemy, flask-cors**
- **mysqlclient**
- **MySQL Server (we use Wamp)**
- **Node.js and npm**

---

## 📦 How to Activate

1. **Clone the Repository**
   ```cmd
   git clone https://github.com/yourusername/money_tracker.git
   cd money_tracker
   ```
2. **Create a Virtual Environment (optional but recommended) and Install Required Dependencies**
   ```cmd
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Activate Vue**
   ```cmd
   cd frontend
   npm install 
   npm run dev
   ```
4. **Activate Flask**
   ```cmd
   flask run
   ```
Note: Ensure both the Flask backend and Vue.js frontend servers are running simultaneously.

## 👤 Author
Made with ❤️ by **Celine Vania Setiadi**, **Joanna Gracia Tan**, **Brygitta Josephine Makarawung**  
GitHub: 
- Celine: [@celinevs](https://github.com/celinevs)
- Joanna: [@joanna00329](https://github.com/joanna00329)
- Brygitta: [@brygittajosefien](https://github.com/brygittaa)
