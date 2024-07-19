import streamlit as st
from hpc_manager import RemoteProjectFileSystem

@st.cache_resource
def get_fs(host, username, password):
    fs = RemoteProjectFileSystem(host, username, password, protocol= 'sftp')
    return fs