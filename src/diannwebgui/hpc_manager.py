from fs.errors import ResourceNotFound
from fs.sshfs import SSHFS
from fs.ftpfs import FTPFS


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


if __name__ == "__main__":
    # Connect to FTP server

    # Alternatively, connect to SFTP server
    pfs = RemoteProjectFileSystem('login02.scripps.edu', 'username', 'password', protocol='sftp')

    # Create a new project with metadata
    pfs.create_project('project1', {'author': 'John Doe', 'description': 'Sample project'})

    # Add a data file to the project
    pfs.add_data_file('project1', 'data1.txt', 'This is some sample data.')

    # List all projects
    projects = pfs.list_projects()
    print(projects)

    # List all data files in a project
    data_files = pfs.list_data_files('project1')
    print(data_files)

    # Remove a project
    pfs.remove_project('project1')