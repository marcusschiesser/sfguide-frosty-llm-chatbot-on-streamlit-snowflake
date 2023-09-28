import openai
import streamlit as st
from charts import render_data
from editor import parse_sql, render_sql
from examples import render_examples
from prompts import get_inital_messages

st.title("☃️ Frosty")

# Initialize the chat messages history
openai.api_key = st.secrets.OPENAI_API_KEY
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = get_inital_messages()

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

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


if num_messages == 2:  # bot just said hello
    example = render_examples()
    if example:
        st.session_state.messages.append({"role": "user", "content": example})
        with st.chat_message("user"):
            st.write(example)


def get_response(container):
    response = ""
    for delta in openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
        response += delta.choices[0].delta.get("content", "")
        container.markdown(response)
    return response


# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        resp_container = st.empty()
        response = get_response(resp_container)

        message = {"role": "assistant", "content": response}

        # Parse the response for a SQL query
        if sql_match := parse_sql(response):
            message["sql_match"] = sql_match
        st.session_state.messages.append(message)
        st.experimental_rerun()
