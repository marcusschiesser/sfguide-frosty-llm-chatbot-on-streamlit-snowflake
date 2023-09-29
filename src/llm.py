import openai
import streamlit as st

openai.api_key = st.secrets.OPENAI_API_KEY

SEND_EXAMPLE_RESPONSE = False

EXAMPLE_RESPONSE = """
Sure, in order to get the total value of "All Real Estate Loans" per bank for the year 2020, we can group by the entity (or bank) and sum the value. Here's the SQL command to achieve this:

```sql
SELECT 
    ENTITY_NAME, 
    SUM(VALUE) AS TOTAL_REAL_ESTATE_LOANS 
FROM FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES
WHERE 
    VARIABLE_NAME ilike '%All Real Estate Loans%'
    AND YEAR = 2020
GROUP BY ENTITY_NAME 
LIMIT 10;
```
This query will return the total value of all real estate loans for each bank (entity name) in 2020.
"""


def get_example_response(container):
    container.markdown(EXAMPLE_RESPONSE)
    return EXAMPLE_RESPONSE


def get_response(container):
    if SEND_EXAMPLE_RESPONSE:
        return get_example_response(container)
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
