import streamlit as st
import pandas as pd
import numpy as np
from hpc_manager import RemoteProjectFileSystem

from utils import get_fs

st.title("Upload Search")

fs = get_fs()

selected_project = st.selectbox("Select Project:", options=fs.list_projects())

@st.experimental_dialog("Upload Search")
def upload_prompt():
    search_name = st.text_input("Search Name:")

    search_parameters = {}

    search_parameters['fdr'] = st.number_input("Precursor FDR (%):", min_value=0, max_value=100, value=1)
    search_parameters['additional_options'] = st.text_input("Additional Options:")
    search_parameters['mass_accuracy'] = st.number_input("Mass accuracy:", min_value=0, max_value=100, value=0)
    search_parameters['ms1_accuracy'] = st.number_input("MS1 accuracy:", min_value=0, max_value=100, value=0)
    search_parameters['scan_window'] = st.number_input("Scan window:", min_value=0, max_value=100, value=0)
    search_parameters['unrelated_runs'] = st.checkbox("Unrelated runs", value=False)
    search_parameters['peptidoforms'] = st.checkbox("Peptidoforms", value=False)
    search_parameters['mbr'] = st.checkbox("MBR", value=False)
    search_parameters['heuristic_protein_interface'] = st.checkbox("Heuristic protein interface", value=True)
    search_parameters['no_shared_spectra'] = st.checkbox("No shared spectra", value=True)
    search_parameters['protein_inference'] = st.selectbox("Protein inference:", options=["Genes", "Isoform IDs", "Protein names (from FASTA)", "Genes (species-specific)", "Off"])
    search_parameters['neural_network_classifier'] = st.selectbox("Neural network classifier:", options=["Single-pass mode", "Off", "Double-pass mode"])

    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm Search", use_container_width=True, type='primary'):
            fs.add_search(selected_project, search_name, search_parameters)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary'):
            st.rerun()

if st.button("Configure Search Parameters", use_container_width=True, type='primary'):
    upload_prompt()