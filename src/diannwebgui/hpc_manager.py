from fs.errors import ResourceNotFound
from fs.sshfs import SSHFS
from fs.ftpfs import FTPFS
import json
from fs.errors import ResourceNotFound, DirectoryExists


class RemoteProjectFileSystem:
    def __init__(self, host, user, passwd, protocol='ftp'):
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

    def create_project(self, project_name):
        project_path = f'{project_name}'
        if self.project_fs.exists(project_path):
            raise FileExistsError(f"Project '{project_name}' already exists.")

        project_fs = self.project_fs.makedir(project_path)
        project_fs.makedir('data')
        project_fs.makedir('search')
        project_fs.makedir('spec_lib')

    def add_data_file(self, project_name, file_name, data):
        data_path = f'{project_name}/data/{file_name}'
        if not self.project_fs.exists(f'{project_name}/data'):
            raise ResourceNotFound(f"Project '{project_name}' does not exist or has no 'data' directory.")

        with self.project_fs.open(data_path, 'w') as data_file:
            data_file.write(data)

    def move_data_file(self, project_name, file_name, new_file_name, move: bool = True):
        data_path = f'{project_name}/data/{file_name}'
        new_data_path = f'{project_name}/data/{new_file_name}'
        if not self.project_fs.exists(data_path):
            raise ResourceNotFound(f"Data file '{file_name}' not found in project '{project_name}'.")

        if move:
            self.project_fs.move(data_path, new_data_path)
        else:
            self.project_fs.copy(data_path, new_data_path)

    def remove_data_file(self, project_name, file_name):
        data_path = f'{project_name}/data/{file_name}'
        if not self.project_fs.exists(data_path):
            raise ResourceNotFound(f"Data file '{file_name}' not found in project '{project_name}'.")

        self.project_fs.remove(data_path)

    def list_projects(self):
        return self.project_fs.listdir('.')

    def list_data_files(self, project_name):
        data_dir = f'{project_name}/data'
        if not self.project_fs.exists(data_dir):
            raise ResourceNotFound(f"No data directory found for project '{project_name}'.")
        return self.project_fs.listdir(data_dir)

    def remove_project(self, project_name):
        project_path = f'{project_name}'
        if self.project_fs.exists(project_path):
            self.project_fs.removetree(project_path)
        else:
            raise ResourceNotFound(f"Project '{project_name}' does not exist.")

    def add_spec_lib(self, project_name, file_name, data):
        data_path = f'{project_name}/spec_lib/{file_name}'
        spec_lib_dir = f'{project_name}/spec_lib'

        if not self.project_fs.exists(spec_lib_dir):
            raise ResourceNotFound(f"Project '{project_name}' does not exist or has no 'data' directory.")

        # Check if any file already exists in the spec_lib directory
        if self.project_fs.listdir(spec_lib_dir):
            raise FileExistsError(f"A spec lib file already exists in project '{project_name}'.")

        with self.project_fs.open(data_path, 'w') as data_file:
            data_file.write(data)

    def remove_spec_lib(self, project_name):
        spec_lib_dir = f'{project_name}/spec_lib'

        if not self.project_fs.exists(spec_lib_dir):
            raise ResourceNotFound(f"Project '{project_name}' does not exist or has no 'spec_lib' directory.")

        # List all files in the spec_lib directory
        files = self.project_fs.listdir(spec_lib_dir)

        if not files:
            raise ResourceNotFound(f"No spec lib files found in project '{project_name}'.")

        # Remove each file in the spec_lib directory
        for file in files:
            file_path = f'{spec_lib_dir}/{file}'
            self.project_fs.remove(file_path)

        print(f"Removed spec lib files from project '{project_name}'.")

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
        config_path = f'{search_dir}/config.json'
        with self.project_fs.open(config_path, 'w') as config_file:
            json.dump(data, config_file)

        print(f"Search '{search_name}' added to project '{project_name}'.")

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

        print(f"Search '{search_name}' removed from project '{project_name}'.")


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