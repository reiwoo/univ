import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.write("## TASK1:")
columns = [f"col {i}" for i in range(1, 5)]
rows = [f"row {i}" for i in range(1, 5)]
df = pd.DataFrame(np.random.randint(1, 100, size=(len(rows), len(columns))),columns=columns,index=rows)
df
st.write("## TASK2:")
TEXT = "Hello Streamlit"
def stream_data():
    for word in TEXT.split(" "):
        yield word + " "
        time.sleep(1)
if st.button("Stream data"):
    st.write_stream(stream_data)

"""
## TASK 3
Используем Streamlit для визуализации данных!
"""
arr = np.random.normal(0, 1, size=1000)
fig, ax = plt.subplots()
ax.hist(arr, bins=30)
ax.set_title("hist normal")
fig