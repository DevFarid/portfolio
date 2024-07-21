import configparser
import os
import git # type: ignore
import requests # type: ignore
from collections import defaultdict
import markdown # type: ignore

class project:

    def __init__(self, name, clazz: str = None):
        self.name = name
        self.repoLink = None
        self.date = None
        self.lastCommit = None
        self.numOfCommits = None
        self.relative_path = ""
        self.languagesUsed = []
        self.readmeContents = None
        self.shortDescription = None

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
        self.loadReadme()
        self.loadShortDescription()

    def loadIcon(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
        x = Utilities.get_project_info(dir_path, 'url')
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

    def loadReadme(self):
        x = None
        read_me_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path), 'README.md')
        if not os.path.exists(read_me_path):
            return None
        with open(read_me_path, "r", encoding='utf-8') as md_file:
            md_content = md_file.read()
            x = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])
            if x is not None:
                self.readmeContents = x

    def loadShortDescription(self):
        x = None
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
        x = Utilities.get_project_info(dir_path, 'desc')
        if x is not None:
            self.shortDescription = x

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
    
    def getReadME(self):
        return self.readmeContents
    
    def hasReadME(self):
        return self.readmeContents is not None
    
    def getShortDescription(self):
        return self.shortDescription

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
        '.sh': 'Shell'
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
    def get_project_info(directory, key):
        filePath = Utilities.fileExists(directory, '.portfolio')
        if filePath is not None:
            with open(filePath, 'r', encoding='utf-8') as config_file:
                config_content = config_file.read()

                config_parser = configparser.ConfigParser()
                config_parser.read_string(config_content)

                try:
                    logolink = config_parser.get('proj_config', key)
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


    @staticmethod
    def read_experience_config(directory):
        experience_file = Utilities.fileExists(directory, '.experience')
        if experience_file is None:
            return None
        config = configparser.ConfigParser()
        with open(experience_file, 'r', encoding='utf-8') as file:
            config.read_file(file)
        title = config['experience_config']['title']
        date = config['experience_config']['date']
        n = int(config['experience_config']['n'])
        job_functions = [config['experience_config'][f'jobFunction{i}'] for i in range(n)]
        return title, date, job_functions
    
    @staticmethod
    def get_formal_name(directory):
        fileExists = Utilities.fileExists(directory, '.class')
        if fileExists is None:
            return None
        config = configparser.ConfigParser()
        with open(fileExists, 'r', encoding='utf-8') as file:
            config.read_file(file)
        return config['class_config']['formal_name']
    
    @staticmethod
    def list_directories(dir_path):
        try:
            # List all entries in the directory
            entries = os.listdir(dir_path)
            
            # Filter out non-directories and the __pycache__ directory
            directories = [
                entry for entry in entries
                if os.path.isdir(os.path.join(dir_path, entry)) and entry != '__pycache__'
            ]
            
            return directories
        
        except FileNotFoundError:
            print(f"Error: The directory {dir_path} does not exist.")
            return []
        except PermissionError:
            print(f"Error: Permission denied to access {dir_path}.")
            return []