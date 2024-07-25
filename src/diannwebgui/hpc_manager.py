from fs.sshfs import SSHFS
from fs.ftpfs import FTPFS
from fs.errors import ResourceNotFound, DirectoryExists
import json
from fs.path import join
from fs.osfs import OSFS

import streamlit as st
import pandas as pd

from src.diannwebgui.pages.gui import create_scp_client
from utils import get_fs
import paramiko
from scp import SCPClient

class RemoteProjectFileSystem:
    def __init__(self, host, user, passwd, protocol='ftp'):
        self._user = user
        home_path = f'/gpfs/home/{user}'  # Adjust as necessary
        if protocol == 'ftp':
            self.fs = FTPFS(host, user, passwd)
        elif protocol == 'sftp':
            self.fs = SSHFS(host, user=user, passwd=passwd)
        else:
            raise ValueError("Unsupported protocol. Use 'ftp' or 'sftp'.")

        home_fs = self.fs.opendir(home_path)
        if not home_fs.exists('projects'):
            home_fs.makedir('projects')

        self.project_fs = home_fs.opendir('projects')

    def get_user(self):
        return self._user

    def get_data_file_contents(self, project_name, file_name):
        file_path = f'{project_name}/data/{file_name}'
        with self.project_fs.open(file_path, 'r') as file:
            return file.read()

    def get_spec_lib_contents(self, project_name, file_name):
        file_path = f'{project_name}/spec_lib/{file_name}'
        with self.project_fs.open(file_path, 'r') as file:
            return file.read()

    def get_search_contents(self, project_name, search_name, file_name):
        file_path = f'{project_name}/search/{search_name}/{file_name}'
        with self.project_fs.open(file_path, 'r') as file:
            return file.read()

    def create_project(self, project_name):
        project_path = f'{project_name}'
        if self.project_fs.exists(project_path):
            raise FileExistsError(f"Project '{project_name}' already exists.")

        project_fs = self.project_fs.makedir(project_path)
        project_fs.makedir('data')
        project_fs.makedir('search')
        project_fs.makedir('spec_lib')

    def remove_project(self, project_name):
        project_path = f'{project_name}'
        if self.project_fs.exists(project_path):
            self.project_fs.removetree(project_path)
        else:
            raise ResourceNotFound(f"Project '{project_name}' does not exist.")

    def list_projects(self):
        return self.project_fs.listdir('.')

    def add_data_file(self, project_name, file_name, data):
        data_path = f'{project_name}/data/{file_name}'
        if not self.project_fs.exists(f'{project_name}/data'):
            raise ResourceNotFound(f"Project '{project_name}' does not exist or has no 'data' directory.")

        with self.project_fs.open(data_path, 'w') as data_file:
            data_file.write(data)

    def remove_data_file(self, project_name, file_name):
        data_path = f'{project_name}/data/{file_name}'
        if not self.project_fs.exists(data_path):
            raise ResourceNotFound(f"Data file '{file_name}' not found in project '{project_name}'.")

        self.project_fs.remove(data_path)

    def list_data_files(self, project_name):
        data_dir = f'{project_name}/data'
        if not self.project_fs.exists(data_dir):
            raise ResourceNotFound(f"No data directory found for project '{project_name}'.")
        return self.project_fs.listdir(data_dir)

    def add_spec_lib(self, project_name, file_name, data):
        spec_lib_path = f'{project_name}/spec_lib/{file_name}'
        if not self.project_fs.exists(f'{project_name}/spec_lib'):
            raise ResourceNotFound(f"Project '{project_name}' does not exist or has no 'spec_lib' directory.")

        with self.project_fs.open(spec_lib_path, 'w') as spec_lib_file:
            spec_lib_file.write(data)

    def remove_spec_lib(self, project_name, file_name):
        spec_lib_path = f'{project_name}/spec_lib/{file_name}'
        if not self.project_fs.exists(spec_lib_path):
            raise ResourceNotFound(f"Spectral library file '{file_name}' not found in project '{project_name}'.")

        self.project_fs.remove(spec_lib_path)

    def list_spec_lib_files(self, project_name):
        spec_lib_dir = f'{project_name}/spec_lib'
        if not self.project_fs.exists(spec_lib_dir):
            raise ResourceNotFound(f"No spectral library directory found for project '{project_name}'.")
        return self.project_fs.listdir(spec_lib_dir)

    def add_search(self, project_name, search_name, data):
        project_dir = f'{project_name}'
        search_dir = f'{project_name}/search/{search_name}'

        # Check if the project exists
        if not self.project_fs.exists(project_dir):
            raise ResourceNotFound(f"Project '{project_name}' does not exist.")

        # Check if the search directory already exists
        if self.project_fs.exists(search_dir):
            raise DirectoryExists(f"Search '{search_name}' already exists in project '{project_name}'.")

        # Create the search directory
        self.project_fs.makedir(search_dir, recreate=True)

        # Save data to the new folder as config.json
        # config_path = f'{search_dir}/config.json'
        # with self.project_fs.open(config_path, 'w') as config_file:
        #     json.dump(data, config_file)

        # TODO: add command additions from the "Precursor Ion Generation" section of DIA-NN
        command = ""

        data_directory = f'{project_name}/data'
        data_files = self.project_fs.listdir(data_directory)
        for data_file in data_files:
            command += f" --f {data['projects_path']}/{data_directory}/{data_file}"

        spec_lib_directory = f'{project_name}/spec_lib'
        spec_lib_files = self.project_fs.listdir(spec_lib_directory)
        for spec_lib_file in spec_lib_files:
            command += f" --lib {data['projects_path']}/{spec_lib_directory}/{spec_lib_file}"

        command += " --verbose " + str(data['log_level'])
        command += " --out " + data['projects_path'] + "/" + search_dir
        command += " --qvalue " + str(data['precursor_fdr']/100)

        if data['quantities_matrices']:
            command += " --matrices"

        if data['speed_and_ram_usage'] == "Low RAM usage":
            command += " --min-corr 1.0 --corr-diff 1.0 --time-corr-only"
        elif data['speed_and_ram_usage'] == "Low RAM & high speed":
            command += " --min-corr 2.0 --corr-diff 1.0 --time-corr-only"
        elif data['speed_and_ram_usage'] == "Ultra-fast":
            command += " --min-corr 2.0 --corr-diff 1.0 --time-corr-only --extracted-ms1"

        if data['prosit']:
            command += " --prosit"
        if data['xics']:
            command += " --xic"

        command += " --unimod4"

        if data['scan_window'] != 0:
            command += " --window " + str(data['scan_window'])
        if data['mass_accuracy'] != 0:
            command += " --mass-acc " + str(data['mass_accuracy'])
        if data['ms1_accuracy'] != 0:
            command += " --mass-acc-ms1 " + str(data['ms1_accuracy'])

        if (data['neural_network_classifier'] == "Double-Pass Mode"):
            command += " --double-search"
        elif (data['neural_network_classifier'] == "Off"):
            command += " --no-nn"

        if data['unrelated_runs']:
            command += " --individual-mass-acc --individual-windows"
        if data['peptidoforms']:
            command += " --peptidoforms"

        if not data['no_shared_spectra']:
            command += " --int-removal 0"

        if data['mbr']:
            command += " --reanalyse"

        if ['heuristic_protein_interface']:
            command += " --relaxed-prot-inf"

        if (data['library_generation'] == "IDs profiling"):
            command += " --id-profiling"
        elif (data['library_generation'] == "IDs, RT and IM profiling"):
            command += " --rt-profiling"
        elif (data['library_generation'] == "Smart profiling"):
            command += " --smart-profiling"

        if (data['protein_inference'] == "Isoform IDs"):
            command += " --pg-level 0"
        elif (data['protein_inference'] == "Protein Names (from FASTA)"):
            command += " --pg-level 1"
        elif (data['protein_inference'] == "Genes (Species-Specific)"):
            command += " --pg-level 2 --species-genes"
        elif (data['protein_inference'] == "Off"):
            command += " --no-prot-inf"

        if (data['quantification_strategy'] == "Legacy (direct)"):
            command += " --direct-quant"
        elif (data['quantification_strategy'] == "QuantUMS (high accuracy)"):
            command += " --high-acc"

        if (data['cross-run_normalization'] == "Global"):
            command += " --global-norm"
        elif (data['cross-run_normalization'] == "RT & signal-dep. (experimental)"):
            command += " --sig-norm"
        elif (data['cross-run_normalization'] == "Off"):
            command += " --no-norm"

        if not (data['additional_options'] == ""):
            command += " " + data['additional_options']

        command_path = f'{search_dir}/command.json'
        with self.project_fs.open(command_path, 'w') as command_file:
            json.dump(command, command_file)

        script = f"""#!/bin/sh
        #SBATCH --nodes=1
        #SBATCH --ntasks=1
        #SBATCH --cpus-per-task=20
        #SBATCH --mem=50Gb
        #SBATCH --partition=highmem
        #SBATCH --time=240:00:00

        cd $SLURM_SUBMIT_DIR

        /gpfs/home/rpark/cluster/DiaNN.sif --threads 20 {command}
        """
        script_replaced = script.replace("\r\n", "\n").replace("\r", "\n")
        script_path = f"{project_name}/search/{search_name}/search_command.sh"

        with self.project_fs.open(script_path, 'w') as search_command_file:
            search_command_file.write(script_replaced)

    def run_search(self, project_name, search_name):
        ssh = create_scp_client(st.session_state['server_ip'], st.session_state['username'], st.session_state['password'])

        home_fs = OSFS('~/')
        projects_path = home_fs.getsyspath('projects')

        script_path = f"{projects_path}/{project_name}/search/{search_name}/search_command.sh"
        ssh.exec_command(f"chmod +x {script_path}")
        stdin, stdout, stderr = ssh.exec_command(f"sbatch {script_path}")
        st.write(stderr.read().decode())
        ssh.close()

    def remove_search(self, project_name, search_name):
        project_dir = f'{project_name}'
        search_dir = f'{project_name}/search/{search_name}'

        # Check if the project exists
        if not self.project_fs.exists(project_dir):
            raise ResourceNotFound(f"Project '{project_name}' does not exist.")

        # Check if the search directory exists
        if not self.project_fs.exists(search_dir):
            raise ResourceNotFound(f"Search '{search_name}' does not exist in project '{project_name}'.")

        # Remove the search directory and its contents
        self.project_fs.removetree(search_dir)

    def list_searches(self, project_name):
        search_dir = join(project_name, 'search')
        if not self.project_fs.exists(search_dir):
            raise ResourceNotFound(f"No search directory found for project '{project_name}'.")
        return self.project_fs.listdir(search_dir)

if __name__ == "__main__":
    # Connect to FTP server
    password = input("Enter password: ")

    # Alternatively, connect to SFTP server
    pfs = RemoteProjectFileSystem('login02.scripps.edu', 'pgarrett', password, protocol='sftp')

    # Create a new project with metadata
    pfs.create_project('project1')

    # Add a data file to the project
    pfs.add_data_file('project1', 'data1.txt', 'This is some sample data.')

    # List all projects
    projects = pfs.list_projects()
    print(projects)

    # List all data files in a project
    data_files = pfs.list_data_files('project1')
    print(data_files)

    # Add a search to the project
    try:
        pfs.add_search('project1', 'search1', {'param1': 'value1', 'param2': 'value2'})
    except Exception as e:
        print(e)

    # Attempt to add the same search to the project to test error handling
    try:
        pfs.add_search('project1', 'search1', {'param1': 'value1', 'param2': 'value2'})
    except Exception as e:
        print(e)

    print(pfs.get_search_path('project1', 'search1'))

    # Remove the search from the project
    try:
        pfs.remove_search('project1', 'search1')
    except Exception as e:
        print(e)

    # Attempt to remove a non-existent search to test error handling
    try:
        pfs.remove_search('project1', 'search1')
    except Exception as e:
        print(e)

    # Remove a project
    pfs.remove_project('project1')