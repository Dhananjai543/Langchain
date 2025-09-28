import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent, AgentType
from langchain.sql_database import SQLDatabase
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="💬 Chat with SQL Database", page_icon="💬")
st.title("💬 Chat with SQL Database")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLite 3 Database","Connect to your MySQL Database"]

selected_opt=st.sidebar.radio("Choose the DB you want to chat with",options=radio_opt)


if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Enter your MySQL Host")
    mysql_user=st.sidebar.text_input("Enter your MySQL User")
    mysql_password=st.sidebar.text_input("Enter your MySQL Password",type="password")
    mysql_database=st.sidebar.text_input("Enter your MySQL Database")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input("Enter your Groq API Key", type="password")

if not db_uri:
    st.info("Please select the database option to continue.")

if not api_key:
    st.info("Please enter your Groq API Key to continue.")

# LLM Model
llm = ChatGroq(groq_api_key=api_key, model="qwen/qwen3-32b", streaming=True)

st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_database=None):
    if db_uri==LOCALDB:
        db_path = (Path(__file__).parent / "student.db").resolve()
        if not db_path.exists():
            st.error("SQLite database file 'student.db' not found. Please ensure the database file is in the correct location.")
            st.stop()
        creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite://", creator=creator))
    else:
        if not all([mysql_host, mysql_user, mysql_password, mysql_database]):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}")
        db = SQLDatabase(engine)
    return db


if db_uri==MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_database)
else:
    db = configure_db(db_uri)

# Create the toolkit and agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
    

if "messages" not in st.session_state or st.sidebar.button("Clear Conversation"):
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="What would you like to ask?")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)