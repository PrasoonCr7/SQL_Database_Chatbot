import streamlit as st  # Web app UI
from pathlib import Path # Helps find student.db file
from langchain.agents import create_sql_agent # Build smart sql agent that talk with db 
from langchain.sql_database import SQLDatabase # Langchain work with sdl database 
from langchain.agents.agent_types import AgentType 
from langchain.callbacks import StreamlitCallbackHandler # shows live agent thinking in UI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit # Give the agent DB tools
from sqlalchemy import create_engine # Connect to database
import sqlite3 # Connect to sqlite
from langchain_groq import ChatGroq # Use Groq model LLama 3 as AI Brain

# Set a page title in the browser tab.
# Adds a big heading at the top of the app.
st.set_page_config(page_title="LangChain: Chat with SQL DB")
st.title("Langchain: Chat with SQL DB")

# Constants
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# Sidebar UI
# Use local SQLite database (student.db)
# Connect to MySQL database
radio_opt = ["Use SQLLite 3 Database - Student.db", "Connect to your SQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB you want to chat with", options=radio_opt)

# Database connection input
if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host", value="localhost")
    mysql_user = st.sidebar.text_input("MySQL User", value="root")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database", value="student")
else:
    db_uri = LOCALDB
    mysql_host = mysql_user = mysql_password = mysql_db = None  # Clear out

# Groq API Key
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Please add your Groq API Key to continue.")
    st.stop()

# LLM setup
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# Configure DB
# SQLite: Loads student.db from your local folder.
# MySQL: Uses provided credentials to connect.
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(
            create_engine(
                f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            )
        )

# Call DB config
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

# Setup LangChain toolkit + agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Session state
if "messages" not in st.session_state or st.sidebar.button("Clear chat"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_query = st.chat_input("Ask something from the database")

if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(user_query, callbacks=[callback])
            st.session_state["messages"].append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            st.error(f" Error: {str(e)}")