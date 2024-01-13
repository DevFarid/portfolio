import configparser
import os

class project:

    def __init__(self, name, clazz: str = None, isClassProject: bool = False):
        self.name = name
        self.repoLink = None
        self.date = None

        self.relative_path = ""

        self.icon = None

        if isClassProject and clazz is not None:
            self.relative_path = "classes\\" + clazz + "\\" + name
        else:
            self.relative_path = "projects\\" + name
            
        self.loadIcon()
        self.loadRepoLink()

    def loadIcon(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.relative_path)
        x = Utilities.get_project_icon(dir_path)
        if x is None:
            pass
        else:
            self.icon = x

    def getIcon(self):
        return self.icon

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

class Utilities:
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