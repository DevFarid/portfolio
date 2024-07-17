import configparser
import os
import git # type: ignore
import requests # type: ignore

class project:

    def __init__(self, name, clazz: str = None, isClassProject: bool = False):
        self.name = name
        self.repoLink = None
        self.date = None
        self.lastCommit = None

        self.relative_path = ""

        self.icon = None

        if isClassProject and clazz is not None:
            self.relative_path = "classes\\" + clazz + "\\" + name
        else:
            self.relative_path = "projects\\" + name
            
        self.loadIcon()
        self.loadRepoLink()
        self.loadGitDate()
        self.loadLastCommit()

    def loadGitDate(self):
        if self.repoLink is not None:
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
            x = Utilities.get_creation_date(dir_path)
            if x is not None:
                self.date = x

    def loadLastCommit(self):
        if self.repoLink is not None:
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
            x = Utilities.get_last_commit_date(dir_path)
            if x is not None:
                self.lastCommit = x

    def loadIcon(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
        x = Utilities.get_project_icon(dir_path)
        if x is None:
            pass
        else:
            self.icon = x

    def loadRepoLink(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
        x = Utilities.get_project_git_config_url(dir_path)
        if x is None:
            pass
        else:
            self.repoLink = x

    def getRepoLink(self):
        return self.repoLink

    def getName(self):
        return self.name

    def getIcon(self):
        return self.icon

    def hasIcon(self):
        return self.icon is not None

    def getCreatedDate(self):
        return self.date

    def getLastCommit(self):
        return self.lastCommit

class Utilities:
    @staticmethod
    def get_repo_info(repo_url):
        response = requests.get(f"https://api.github.com/repos/{repo_url}")
        if response.status_code == 200:
            repo_data = response.json()
            return repo_data

    @staticmethod
    def fileExists(directory, configFile):
        filePath = os.path.join(directory, configFile)
        if not os.path.exists(filePath):
            return None
        return filePath

    @staticmethod
    def get_project_git_config_url(directory):
        directory = os.path.join(directory, ".git")
        filePath = Utilities.fileExists(directory, 'config')
        if filePath is not None:
            with open(filePath, 'r', encoding='utf-8') as config_file:
                config_content = config_file.read()

                config_parser = configparser.ConfigParser()
                config_parser.read_string(config_content)
            
                # Get the URL from the parsed config
                try:
                    url = config_parser.get('remote "origin"', 'url')
                    return url
                except (configparser.NoSectionError, configparser.NoOptionError) as e:
                    return None
                    # raise ValueError(f"Failed to retrieve URL from git config: {e}")

    @staticmethod 
    def get_project_version(directory):
        filePath = Utilities.fileExists(directory, 'pyproject.toml')
        if filePath is not None:
            with open(filePath, 'r', encoding='utf-8') as config_file:
                config_content = config_file.read()

                config_parser = configparser.ConfigParser()
                config_parser.read_string(config_content)

                try:
                    v = config_parser.get('tool.commitizen', 'version')
                    return v
                except (configparser.NoSectionError, configparser.NoOptionError) as e:
                    return None
                    # raise ValueError(f"Failed to retrieve version from pyproject.toml: {e}")
    
    @staticmethod
    def get_project_icon(directory):
        filePath = Utilities.fileExists(directory, 'logoconfig')
        if filePath is not None:
            with open(filePath, 'r', encoding='utf-8') as config_file:
                config_content = config_file.read()

                config_parser = configparser.ConfigParser()
                config_parser.read_string(config_content)

                try:
                    logolink = config_parser.get('logoconfig', 'url')
                    return logolink
                except (configparser.NoSectionError, configparser.NoOptionError) as e:
                    return None

    @staticmethod
    def get_last_commit_date(directory):
        if not os.path.isdir(directory):
            return None
        else:
            repo = git.Repo(directory)
            default_branch = repo.head.ref.name
            first_commit = list(repo.iter_commits(default_branch, max_count=1))[0]
            return first_commit.committed_datetime.strftime('%m/%d/%y')

    @staticmethod
    def get_creation_date(directory):
        if not os.path.isdir(directory):
            return None
        else:
            repo = git.Repo(directory)
            default_branch = repo.head.ref.name
            # Get all commits for the branch
            commits = list(repo.iter_commits(default_branch))
            # The last commit in the list is the first ever commit
            first_commit = commits[-1]
            return first_commit.committed_datetime.strftime('%m/%d/%y')

    @staticmethod
    def get_directory_tree(path, depth=0):
        tree = {}
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir():
                    tree[entry.name] = (Utilities.get_directory_tree(entry.path, depth + 1), depth)
                else:
                    tree[entry.name] = (entry.name, depth)
        return tree

    @staticmethod
    def print_tree(tree, depth=0):
        for name, value in tree.items():
            if isinstance(value[0], dict):
                print("  " * depth + f"{name}/ (depth={depth})")
                Utilities.print_tree(value[0], depth + 1)
            else:
                print("  " * depth + f"{name} (depth={depth})")