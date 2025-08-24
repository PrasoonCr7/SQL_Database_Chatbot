# SQL_Database_Chatbot

## Chat with SQL Database (LangChain + Streamlit + Groq)

A smart Streamlit application that allows you to chat with your SQL database in natural language using LangChain and Groq LLM.
Supports both SQLite (student.db) and MySQL databases.

✨ Features

🔹 Chat with your database using natural queries.

🔹 Works with both SQLite and MySQL.

🔹 Uses LangChain SQL Agent for intelligent query generation.

🔹 Powered by Groq LLM (Llama 3).

🔹 Interactive Streamlit chat UI.

📂 Project Structure
📦 sql-chat-app
 ┣ 📜 app.py            # Main Streamlit app
 ┣ 📜 student.db        # Sample SQLite database
 ┣ 📜 requirements.txt  # Dependencies
 ┗ 📜 README.md         # Project documentation

⚙️ Installation

1️⃣ Clone the repo:

git clone https://github.com/your-username/sql-chat-app.git
cd sql-chat-app


2️⃣ Install dependencies:

pip install -r requirements.txt


3️⃣ Run the app:

streamlit run app.py

🔑 Setup

Groq API Key → Enter your key in the sidebar.

SQLite (default) → Uses student.db included in the repo.

MySQL (optional) → Enter connection details in the sidebar.

🎯 Example Queries

"Show all students in section A"

"Who scored the highest marks?"

"What is the average marks in Data Science class?"

"List students with marks greater than 80"

🧩 Tech Stack

Frontend: Streamlit

Backend/Agent: LangChain SQL Agent

Database: SQLite / MySQL

LLM: Groq (Llama 3)
