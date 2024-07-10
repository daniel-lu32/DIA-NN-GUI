import streamlit as st
import pandas as pd
import numpy as np
from hpc_manager import RemoteProjectFileSystem

from utils import get_fs

st.title("Upload Project")

fs = get_fs()

df = pd.DataFrame(fs.list_projects(), columns=['Project'])

st.subheader('Project List')
st.dataframe(df, use_container_width=True, hide_index=True)

@st.experimental_dialog("Add New Project")
def upload_prompt():
    file_name = st.text_input("Project Name:")
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Add", use_container_width=True, type='primary'):
            fs.create_project(file_name)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary'):
            st.rerun()


if st.button("Upload Project", use_container_width=True, type='primary'):
    upload_prompt()