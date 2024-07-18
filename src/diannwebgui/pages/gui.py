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

@st.experimental_dialog("Add Project")
def projects_add_dialogue():
    project_name = st.text_input("Project Name:")
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm", use_container_width=True, type='primary', key="projects_add_dialogue_confirm"):
            fs.create_project(project_name)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary', key="projects_add_dialogue_cancel"):
            st.rerun()

@st.experimental_dialog(f"Are you sure you want to delete these projects?")
def projects_delete_dialogue(df, indices):
    to_be_deleted = st.dataframe(df.iloc[indices]['Projects'], use_container_width=True, hide_index=True)
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm", use_container_width=True, type='primary', key="projects_delete_dialogue_confirm"):
            for index in indices:
                project_name = df.iloc[index]['Projects']
                fs.remove_project(project_name)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary', key="projects_delete_dialogue_cancel"):
            st.rerun()

with t1:
    st.subheader("Projects")
    st.markdown("Click \"Add\" to add a project. To delete, select projects and click \"Delete.\"")
    df = pd.DataFrame(fs.list_projects(), columns=['Projects'])
    selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
    selected_indices = [row for row in selection['selection']['rows']]

    if st.button("Add", use_container_width=True, type='primary', key="projects_add"):
        projects_add_dialogue()
    if st.button("Delete", use_container_width=True, type='secondary', key="projects_delete"):
        if selected_indices:
            projects_delete_dialogue(df, selected_indices)

@st.experimental_dialog("Add Data Files")
def data_add_dialogue():
    data_files = st.file_uploader(label="Upload Data Files", type=[".dia", ".tar", ".zip", ".raw"], accept_multiple_files=True)
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm", use_container_width=True, type='primary', key="data_add_dialogue_confirm"):
            for file in data_files:
                fs.add_data_file(selected_project, file.name, file.getvalue().decode("utf-8"))
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary', key="data_add_dialogue_cancel"):
            st.rerun()

@st.experimental_dialog(f"Are you sure you want to delete these data files?")
def data_delete_dialogue(df, indices):
    to_be_deleted = st.dataframe(df.iloc[indices]['Data Files'], use_container_width=True, hide_index=True)
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm", use_container_width=True, type='primary', key="data_delete_dialogue_confirm"):
            for index in indices:
                file_name = df.iloc[index]['Data Files']
                fs.remove_data_file(selected_project, file_name)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary', key="data_delete_dialogue_cancel"):
            st.rerun()

@st.experimental_dialog("Download Data File")
def data_download_dialogue(df, indices):
    new_file_name = st.text_input("Rename File (Include File Extension):")
    if st.button("Generate Download Link", use_container_width=True, type='primary', key="data_download_dialogue_generate"):
        column1, column2 = st.columns(2)
        with column1:
            selected_files = df.iloc[indices]['Data Files'].tolist()
            st.session_state.selected_files = selected_files
            st.session_state.file_data = {file: fs.get_data_file_contents(selected_project, file) for file in selected_files}
            if st.session_state.selected_files:
                for file in st.session_state.selected_files:
                    file_data = st.session_state.file_data[file]
                    if new_file_name:
                        st.download_button(
                            label=f"Download {new_file_name}",
                            data=file_data,
                            file_name=new_file_name,
                            mime='application/octet-stream',
                            key=f'data_{new_file_name}',
                            use_container_width=True,
                            type='primary'
                        )
                    else:
                        st.download_button(
                            label=f"Download {file}",
                            data=file_data,
                            file_name=file,
                            mime='application/octet-stream',
                            key=f'data_{file}',
                            use_container_width=True,
                            type='primary'
                        )
        with column2:
            if st.button("Cancel", use_container_width=True, type='secondary', key="data_download_dialogue_cancel"):
                st.rerun()

with t2:
    if fs.list_projects():
        st.subheader("Data Files")
        st.markdown("Click \"Add\" to upload data files. To delete, select data files and click \"Delete.\" To download, select ONE data file and click \"Download.\"")
        df = pd.DataFrame(fs.list_data_files(selected_project), columns=['Data Files'])
        selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
        selected_indices = [row for row in selection['selection']['rows']]

        if st.button("Add", use_container_width=True, type='primary', key="data_add"):
            data_add_dialogue()

        column1, column2 = st.columns(2)
        with column1:
            if st.button("Delete", use_container_width=True, type='secondary', key="data_delete"):
                if selected_indices:
                    data_delete_dialogue(df, selected_indices)
        with column2:
            if st.button("Download", use_container_width=True, type='secondary', key="data_download"):
                if selected_indices:
                    data_download_dialogue(df, selected_indices)
@st.experimental_dialog("Add Spectral Libraries")
def spec_lib_add_dialogue():
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

@st.experimental_dialog(f"Are you sure you want to delete these spectral libraries?")
def spec_lib_delete_dialogue(df, indices):
    to_be_deleted = st.dataframe(df.iloc[indices]['Spectral Libraries'], use_container_width=True, hide_index=True)
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm", use_container_width=True, type='primary', key="spec_lib_delete_dialogue_confirm"):
            for index in indices:
                file_name = df.iloc[index]['Spectral Libraries']
                fs.remove_spec_lib(selected_project, file_name)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary', key="spec_lib_delete_dialogue_cancel"):
            st.rerun()

@st.experimental_dialog("Download Spectral Library")
def spec_lib_download_dialogue(df, indices):
    new_file_name = st.text_input("Rename File (Include File Extension):")
    if st.button("Generate Download Link", use_container_width=True, type='primary', key="spec_lib_download_dialogue_generate"):
        column1, column2 = st.columns(2)
        with column1:
            selected_files = df.iloc[indices]['Spectral Libraries'].tolist()
            st.session_state.selected_files = selected_files
            st.session_state.file_data = {file: fs.get_spec_lib_contents(selected_project, file) for file in selected_files}
            if st.session_state.selected_files:
                for file in st.session_state.selected_files:
                    file_data = st.session_state.file_data[file]
                    if new_file_name:
                        st.download_button(
                            label=f"Download {new_file_name}",
                            data=file_data,
                            file_name=new_file_name,
                            mime='application/octet-stream',
                            key=f'data_{new_file_name}',
                            use_container_width=True,
                            type='primary'
                        )
                    else:
                        st.download_button(
                            label=f"Download {file}",
                            data=file_data,
                            file_name=file,
                            mime='application/octet-stream',
                            key=f'data_{file}',
                            use_container_width=True,
                            type='primary'
                        )
        with column2:
            if st.button("Cancel", use_container_width=True, type='secondary', key="data_download_dialogue_cancel"):
                st.rerun()

with t3:
    if fs.list_projects():
        st.subheader("Spectral Libraries")
        st.markdown("Click \"Add\" to upload spectral libraries. To delete, select spectral libraries and click \"Delete.\" To download, select ONE spectral library and click \"Download.\"")
        df = pd.DataFrame(fs.list_spec_lib_files(selected_project), columns=['Spectral Libraries'])
        selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
        selected_indices = [row for row in selection['selection']['rows']]

        if st.button("Add", use_container_width=True, type='primary', key="spec_lib_add"):
            spec_lib_add_dialogue()

        column1, column2 = st.columns(2)
        with column1:
            if st.button("Delete", use_container_width=True, type='secondary', key="spec_lib_delete"):
                if selected_indices:
                    spec_lib_delete_dialogue(df, selected_indices)
        with column2:
            if st.button("Download", use_container_width=True, type='secondary', key="spec_lib_download"):
                if selected_indices:
                    spec_lib_download_dialogue(df, selected_indices)
@st.experimental_dialog("Add Search")
def search_add_dialogue():
    search_name = st.text_input("Search Name:")

    search_parameters = {}
    search_parameters['precursor_fdr'] = st.number_input("Precursor FDR (%):", min_value=0.01, max_value=100.0, value=1.0)
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
@st.experimental_dialog(f"Are you sure you want to delete these searches?")
def search_delete_dialogue(df, indices):
    to_be_deleted = st.dataframe(df.iloc[indices]['Searches'], use_container_width=True, hide_index=True)
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Confirm", use_container_width=True, type='primary', key="search_delete_dialogue_confirm"):
            for index in indices:
                file_name = df.iloc[index]['Searches']
                fs.remove_search(selected_project, file_name)
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary', key="search_delete_dialogue_cancel"):
            st.rerun()

@st.experimental_dialog("Download Search")
def search_download_dialogue(df, indices):
    new_file_name = st.text_input("Rename File (.json):")
    if st.button("Generate Download Link", use_container_width=True, type='primary', key="search_download_dialogue_generate"):
        column1, column2 = st.columns(2)
        with column1:
            selected_files = df.iloc[indices]['Searches'].tolist()
            st.session_state.selected_files = selected_files
            st.session_state.file_data = {file: fs.get_search_contents(selected_project, file, "command.json") for file in selected_files}
            if st.session_state.selected_files:
                for file in st.session_state.selected_files:
                    file_data = st.session_state.file_data[file]
                    if new_file_name:
                        st.download_button(
                            label=f"Download {new_file_name}",
                            data=file_data,
                            file_name=new_file_name,
                            mime='application/octet-stream',
                            key=f'data_{new_file_name}',
                            use_container_width=True,
                            type='primary'
                        )
                    else:
                        st.download_button(
                            label=f"Download command.json",
                            data=file_data,
                            file_name="command.json",
                            mime='application/octet-stream',
                            key=f'data_command.json',
                            use_container_width=True,
                            type='primary'
                        )
        with column2:
            if st.button("Cancel", use_container_width=True, type='secondary', key="data_download_dialogue_cancel"):
                st.rerun()

with t4:
    if fs.list_projects():
        st.subheader("Searches")
        st.markdown("Click \"Add\" to configure search parameters and start a new search. To delete, select searches and click \"Delete.\" To download the command to run DIA-NN, select ONE search and click \"Download.\"")
        df = pd.DataFrame(fs.list_searches(selected_project), columns=['Searches'])
        selection = st.dataframe(df, use_container_width=True, hide_index=True, selection_mode="multi-row", on_select='rerun')
        selected_indices = [row for row in selection['selection']['rows']]

        if st.button("Add", use_container_width=True, type='primary', key="search_add"):
            search_add_dialogue()

        column1, column2 = st.columns(2)
        with column1:
            if st.button("Delete", use_container_width=True, type='secondary', key="search_delete"):
                if selected_indices:
                    search_delete_dialogue(df, selected_indices)
        with column2:
            if st.button("Download", use_container_width=True, type='secondary', key="search_download"):
                if selected_indices:
                    search_download_dialogue(df, selected_indices)