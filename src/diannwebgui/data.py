import streamlit as st
import pandas as pd
import numpy as np
from hpc_manager import RemoteProjectFileSystem

from utils import get_fs

def run():

    st.title("Upload Data")

    fs = get_fs()

    selected_project = st.selectbox("Select Project:", options=fs.list_projects())

    @st.experimental_dialog("Add New Data")
    def upload_prompt():
        data_files = st.file_uploader(label="Upload Data", accept_multiple_files=True)
        column1, column2 = st.columns(2)
        with column1:
            if st.button("Upload", use_container_width=True, type='primary'):
                for file in data_files:
                    fs.add_data_file(selected_project, file.name, file.getvalue().decode("utf-8"))
                st.rerun()
        with column2:
            if st.button("Cancel", use_container_width=True, type='secondary'):
                st.rerun()

    if st.button("Upload Data", use_container_width=True, type='primary'):
        upload_prompt()

    st.subheader('Data File List')
    df = pd.DataFrame(fs.list_data_files(selected_project), columns=['Data Files'])
    st.dataframe(df, use_container_width=True, hide_index=True)
