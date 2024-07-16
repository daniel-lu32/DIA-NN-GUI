import streamlit as st
import pandas as pd
from utils import get_fs

st.title("DIA-NN GUI")
fs = get_fs()

selected_project = st.selectbox("Select Project:", options=fs.list_projects())

t1, t2, t3, t4 = st.tabs(["Projects", "Data Files", "Spectral Libraries", "Searches"])

if 'selected_files' not in st.session_state:
    st.session_state.selected_files = []
if 'file_data' not in st.session_state:
    st.session_state.file_data = {}

with t1:
    st.subheader("Projects")
    df = pd.DataFrame(fs.list_projects(), columns=['Projects'])
    selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
    selected_indices = [row for row in selection['selection']['rows']]
    @st.experimental_dialog("Add Project")
    def add_dialogue():
        project_name = st.text_input("Project Name:")
        column1, column2 = st.columns(2)
        with column1:
            if st.button("Confirm", use_container_width=True, type='primary', key="projects_add_dialogue_confirm"):
                fs.create_project(project_name)
                st.rerun()
        with column2:
            if st.button("Cancel", use_container_width=True, type='secondary', key="projects_add_dialogue_cancel"):
                st.rerun()
    if st.button("Add", use_container_width=True, type='primary', key="projects_add"):
        add_dialogue()
    if st.button("Delete", use_container_width=True, type='secondary', key="projects_delete"):
        for index in selected_indices:
            project_name = df.iloc[index]['Projects']
            fs.remove_project(project_name)
with t2:
    if fs.list_projects():
        st.subheader("Data Files")
        df = pd.DataFrame(fs.list_data_files(selected_project), columns=['Data Files'])
        selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
        selected_indices = [row for row in selection['selection']['rows']]
        @st.experimental_dialog("Add Data Files")
        def add_dialogue():
            data_files = st.file_uploader(label="Upload Data Files", accept_multiple_files=True)
            column1, column2 = st.columns(2)
            with column1:
                if st.button("Confirm", use_container_width=True, type='primary', key="data_add_dialogue_confirm"):
                    for file in data_files:
                        fs.add_data_file(selected_project, file.name, file.getvalue().decode("utf-8"))
                    st.rerun()
            with column2:
                if st.button("Cancel", use_container_width=True, type='secondary', key="data_add_dialogue_cancel"):
                    st.rerun()
        if st.button("Add", use_container_width=True, type='primary', key="data_add"):
            add_dialogue()
        column1, column2 = st.columns(2)
        with column1:
            if st.button("Delete", use_container_width=True, type='secondary', key="data_delete"):
                for index in selected_indices:
                    file_name = df.iloc[index]['Data Files']
                    fs.remove_data_file(selected_project, file_name)
        with column2:
            if st.button("Download", use_container_width=True, type='secondary', key="data_download"):
                selected_files = df.iloc[selected_indices]['Data Files'].tolist()
                st.session_state.selected_files = selected_files
                st.session_state.file_data = {file: fs.get_data_file_contents(selected_project, file) for file in selected_files}
            if st.session_state.selected_files:
                for file in st.session_state.selected_files:
                    file_data = st.session_state.file_data[file]
                    st.download_button(
                        label=f"Download {file}",
                        data=file_data,
                        file_name=file,
                        mime='application/octet-stream',
                        key=f'data_{file}',
                        use_container_width=True
                    )
with t3:
    if fs.list_projects():
        st.subheader("Spectral Libraries")
        df = pd.DataFrame(fs.list_spec_lib_files(selected_project), columns=['Spectral Libraries'])
        selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
        selected_indices = [row for row in selection['selection']['rows']]
        @st.experimental_dialog("Add Spectral Libraries")
        def add_dialogue():
            spec_lib_files = st.file_uploader(label="Upload Spectral Libraries", type=[".txt", ".csv", ".tsv", ".xls", ".speclib", ".sptxt", ".msp"], accept_multiple_files=True)
            column1, column2 = st.columns(2)
            with column1:
                if st.button("Confirm", use_container_width=True, type='primary', key="spec_lib_add_dialogue_confirm"):
                    for file in spec_lib_files:
                        fs.add_spec_lib(selected_project, file.name, file.getvalue().decode("utf-8"))
                    st.rerun()
            with column2:
                if st.button("Cancel", use_container_width=True, type='secondary', key="spec_lib_add_dialogue_cancel"):
                    st.rerun()
        if st.button("Add", use_container_width=True, type='primary', key="spec_lib_add"):
            add_dialogue()
        column1, column2 = st.columns(2)
        with column1:
            if st.button("Delete", use_container_width=True, type='secondary', key="spec_lib_delete"):
                for index in selected_indices:
                    file_name = df.iloc[index]['Spectral Libraries']
                    fs.remove_spec_lib(selected_project, file_name)
        with column2:
            if st.button("Download", use_container_width=True, type='secondary', key="spec_lib_download"):
                selected_files = df.iloc[selected_indices]['Spectral Libraries'].tolist()
                st.session_state.selected_files = selected_files
                st.session_state.file_data = {file: fs.get_spec_lib_contents(selected_project, file) for file in selected_files}
            if st.session_state.selected_files:
                for file in st.session_state.selected_files:
                    file_data = st.session_state.file_data[file]
                    st.download_button(
                        label=f"Download {file}",
                        data=file_data,
                        file_name=file,
                        mime='application/octet-stream',
                        key=f'spec_lib_{file}',
                        use_container_width=True
                    )
with t4:
    if fs.list_projects():
        st.subheader("Searches")
        df = pd.DataFrame(fs.list_searches(selected_project), columns=['Searches'])
        selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
        selected_indices = [row for row in selection['selection']['rows']]
        @st.experimental_dialog("Add Search")
        def add_dialogue():
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
                if st.button("Confirm", use_container_width=True, type='primary', key="search_add_dialogue_confirm"):
                    fs.add_search(selected_project, search_name, search_parameters)
                    st.rerun()
            with column2:
                if st.button("Cancel", use_container_width=True, type='secondary', key="search_add_dialogue_cancel"):
                    st.rerun()

        if st.button("Add", use_container_width=True, type='primary', key="search_add"):
            add_dialogue()
        column1, column2 = st.columns(2)
        with column1:
            if st.button("Delete", use_container_width=True, type='secondary', key="search_delete"):
                for index in selected_indices:
                    file_name = df.iloc[index]['Searches']
                    fs.remove_search(selected_project, file_name)
        with column2:
            if st.button("Download", use_container_width=True, type='secondary', key="search_download"):
                selected_files = df.iloc[selected_indices]['Searches'].tolist()
                st.session_state.selected_files = selected_files
                st.session_state.file_data = {file: fs.get_search_contents(selected_project, file, "command.json") for file in selected_files}
            if st.session_state.selected_files:
                for file in st.session_state.selected_files:
                    file_data = st.session_state.file_data[file]
                    st.download_button(
                        label=f"Download {file}",
                        data=file_data,
                        file_name=f'{file}_command.json',
                        mime='application/octet-stream',
                        key=f'search_{file}',
                        use_container_width=True
                    )