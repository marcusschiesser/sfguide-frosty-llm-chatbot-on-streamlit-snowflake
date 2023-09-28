from dataclasses import dataclass
from typing import Optional
import streamlit as st
from streamlit_monaco import st_monaco
import re


@dataclass
class SQLMatch:
    before: str
    sql: str
    after: str


def parse_sql(response) -> Optional[SQLMatch]:
    sql_match = re.search(r"(.*)```sql\n(.*)\n```(.*)", response, re.DOTALL)
    if sql_match:
        return SQLMatch(
            before=sql_match.group(1),
            sql=sql_match.group(2),
            after=sql_match.group(3),
        )
    return None


def render_sql(sql_match: SQLMatch):
    st.markdown(sql_match.before)
    updated_sql = st_monaco(value=sql_match.sql, height="300px", language="sql")
    st.markdown(sql_match.after)

    if st.button("Run Query"):
        conn = st.experimental_connection("snowpark", ttl="1h")
        return {"data": conn.query(updated_sql)}
    return None
