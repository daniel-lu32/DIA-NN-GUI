import streamlit as st

from hpc_manager import RemoteProjectFileSystem

@st.cache_resource
def get_fs():
    fs = RemoteProjectFileSystem('login02.scripps.edu', 'dalu', 'Pineface3$5^7', protocol='sftp')
    return fs