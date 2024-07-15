import streamlit as st

from hpc_manager import RemoteProjectFileSystem

@st.cache_resource
def get_fs():
    fs = RemoteProjectFileSystem('login02.scripps.edu', '', '', protocol='sftp')
    return fs