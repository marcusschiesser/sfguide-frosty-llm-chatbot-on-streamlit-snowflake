import streamlit as st


EXAMPLES = [
    "What is the total value of all real estate loans per bank in 2020?",
    "Which financial entities have the highest total assets in 2001?",
    "What is the percentage of insured deposits for banks in New York?",
]


def render_examples():
    columns = st.columns(len(EXAMPLES))
    for i, column in enumerate(columns):
        with column:
            if st.button(EXAMPLES[i]):
                return EXAMPLES[i]

    return None


if __name__ == "__main__":
    render_examples()
