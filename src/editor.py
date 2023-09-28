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

    def to_markdown(self) -> str:
        return f"{self.before}```sql\n{self.sql}\n```{self.after}"

    @classmethod
    def parse_markdown(cls, response: str):
        sql_match = re.search(r"(.*)```sql\n(.*)\n```(.*)", response, re.DOTALL)
        if sql_match:
            return cls(
                before=sql_match.group(1),
                sql=sql_match.group(2),
                after=sql_match.group(3),
            )
        return None

    def edit_sql(self) -> Optional[str]:
        st.markdown(self.before)
        updated_sql = st_monaco(value=self.sql, height="300px", language="sql")
        st.markdown(self.after)

        st.write("**You can now edit the query, run it or ask a new question below**")
        if st.button("Run Query"):
            self.sql = updated_sql
            return updated_sql
        return None
