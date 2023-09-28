import streamlit as st
from charts import render_data
from editor import parse_sql, render_sql
from examples import render_examples
from llm import get_response
from prompts import get_inital_messages

st.title("☃️ Frosty")

# Initialize the chat messages history
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = get_inital_messages()


# display the existing chat messages
num_messages = len(st.session_state.messages)
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        if "results" in message:
            st.write(message["content"])
            render_data(key=i, data=message["results"])
        elif i == num_messages - 1 and "sql_match" in message:
            # render the SQL editor for the last message with an SQL match
            if results := render_sql(sql_match=message["sql_match"]):
                message["results"] = results
                st.experimental_rerun()
        else:
            st.write(message["content"])


# If last message is from assistant, prompt for a new question
if st.session_state.messages[-1]["role"] == "assistant":
    # Prompt for user input and save
    if prompt := st.chat_input(placeholder="Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
    # render example questions
    example = render_examples()
    if example:
        st.session_state.messages.append({"role": "user", "content": example})
        with st.chat_message("user"):
            st.write(example)

# If last message is from user, we need to generate a new response
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        resp_container = st.empty()
        response = get_response(resp_container)

        message = {"role": "assistant", "content": response}

        # Parse the response for a SQL query
        if sql_match := parse_sql(response):
            message["sql_match"] = sql_match
        st.session_state.messages.append(message)
        st.experimental_rerun()
