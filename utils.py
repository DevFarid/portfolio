import configparser
import os
import git # type: ignore
import requests # type: ignore
from collections import defaultdict

class project:

    def __init__(self, name, clazz: str = None):
        self.name = name
        self.repoLink = None
        self.date = None
        self.lastCommit = None
        self.numOfCommits = None
        self.relative_path = ""
        self.languagesUsed = []

        self.icon = None

        self.relative_path = "projects\\" + name
        if clazz is not None:
            self.relative_path = "classes\\" + clazz + "\\" + name
            
        self.loadIcon()
        self.loadRepoLink()
        self.loadGitDate()
        self.loadLastCommit()
        self.loadCommits()
        self.loadLanguagesUsed()

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

    def loadCommits(self):
        if self.repoLink is not None:
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
            x = Utilities.get_total_commits(dir_path)
            if x is not None:
                self.numOfCommits = x

    def loadLanguagesUsed(self):
        if self.repoLink is not None:
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
            x = Utilities.get_languages_used(dir_path)
            if x is not None:
                self.languagesUsed = x


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
    
    def getNumOfCommits(self):
        return self.numOfCommits
    
    def getLanguagesUsed(self):
        return ", ".join(self.languagesUsed.keys())

class Utilities:
    EXTENSION_LANGUAGE_MAP = {
        '.py': 'Python',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.cs': 'C#',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.rb': 'Ruby',
        '.go': 'Go',
        '.php': 'PHP',
        '.rs': 'Rust',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.m': 'Objective-C',
        '.pl': 'Perl',
        '.sh': 'Shell',
        # Add more extensions and languages as needed
    }

    @staticmethod
    def get_languages_used(repo_path):
        repo = git.Repo(repo_path)
        languages = defaultdict(int)
        
        # Scan through the working directory for files and their extensions
        for root, _, files in os.walk(repo.working_tree_dir):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in Utilities.EXTENSION_LANGUAGE_MAP:
                    languages[Utilities.EXTENSION_LANGUAGE_MAP[ext]] += 1
        
        return languages

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
    def get_total_commits(directory):
        if not os.path.isdir(directory):
            return None
        else:
            repo = git.Repo(directory)
            default_branch = repo.head.ref.name
            commits = list(repo.iter_commits(default_branch))
            return len(commits)

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
    def retrieve_relative_git_path(directory):
        link = Utilities.get_project_git_config_url(directory)
        if link is not None:
            return link.split("github.com/")[-1].replace('.git', '')

