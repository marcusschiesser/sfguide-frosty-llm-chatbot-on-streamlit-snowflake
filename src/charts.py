from dataclasses import dataclass
import streamlit as st
from streamlit.elements.arrow import Data

DEFAULT_TYPE = 0
CHART_FUNCTIONS = [
    {"label": "Table", "func": st.dataframe},
    {"label": "Line Chart", "func": st.line_chart},
    {"label": "Area Chart", "func": st.area_chart},
    {"label": "Bar Chart", "func": st.bar_chart},
]


@dataclass
class DataResult:
    data: Data
    run_time: float
    type: int = DEFAULT_TYPE

    def render(self, key):
        def set_type(i):
            self.type = i

        columns = st.columns(len(CHART_FUNCTIONS))
        # render chart type buttons
        for i, column in enumerate(columns):
            with column:
                label = CHART_FUNCTIONS[i]["label"]
                key = f"b_{key}_type_{i}"
                st.button(
                    label,
                    key=key,
                    on_click=set_type,
                    args=[i],
                )
        # render chart
        func = CHART_FUNCTIONS[self.type]["func"]
        df = self.data

        st.write(f"Query was running **{self.run_time:.2f} seconds**.")

        # if the function is st.dataframe, just render the dataframe
        if func == st.dataframe:
            st.dataframe(df)
            return
        # if there are more than or two columns, use the first column as the label for the x-axis and the second for the y-axis
        if len(df.columns) >= 2:
            x_axis = df.columns[0]
            y_axis = df.columns[1]
            func(df, x=x_axis, y=y_axis)
        else:
            func(df)
