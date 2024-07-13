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

    search_parameters['precursor_fdr'] = st.number_input("Precursor FDR (%):", min_value=0.01, max_value=100.0, value=1.0)
    search_parameters['threads'] = st.number_input("Threads (%):", min_value=1, max_value=8, value=8)
    search_parameters['log_level'] = st.number_input("Log Level (%):", min_value=0, max_value=5, value=1)
    search_parameters['quantities_matrices'] = st.checkbox("Quantities Matrices", value=True)
    search_parameters['prosit'] = st.checkbox("Generate Prosit Input from FASTA or Spectral Library", value=False)
    search_parameters['xics'] = st.checkbox("XICs", value=False)
    search_parameters['additional_options'] = st.text_input("Additional Options:")
    search_parameters['mass_accuracy'] = st.number_input("Mass Accuracy:", min_value=0, max_value=100, value=0)
    search_parameters['ms1_accuracy'] = st.number_input("MS1 Accuracy:", min_value=0, max_value=100, value=0)
    search_parameters['scan_window'] = st.number_input("Scan Window:", min_value=0, max_value=1000, value=0)
    search_parameters['unrelated_runs'] = st.checkbox("Unrelated Runs", value=False)
    search_parameters['peptidoforms'] = st.checkbox("Peptidoforms", value=False)
    search_parameters['mbr'] = st.checkbox("MBR", value=False)
    search_parameters['heuristic_protein_interface'] = st.checkbox("Heuristic Protein Interface", value=True)
    search_parameters['no_shared_spectra'] = st.checkbox("No Shared Spectra", value=True)
    search_parameters['protein_inference'] = st.selectbox("Protein Inference:", options=["Genes", "Isoform IDs", "Protein Names (from FASTA)", "Genes (Species-Specific)", "Off"])
    search_parameters['neural_network_classifier'] = st.selectbox("Neural Network Classifier:", options=["Single-Pass Mode", "Off", "Double-Pass Mode"])

    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm Search", use_container_width=True, type='secondary'):
            fs.add_search(selected_project, search_name, search_parameters)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='primary'):
            st.rerun()

if st.button("Configure Search Parameters", use_container_width=True, type='primary'):
    upload_prompt()