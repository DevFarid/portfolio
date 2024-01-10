import configparser
import os

class project:

    def __init__(self, name):
        self.name = name
        self.repoLink = None
        self.date = None
        
        # Object/Video Object/idk?? ideas.
        self.showcase = None

        self.loadRepoLink()

    def loadRepoLink(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.name)
        x = self.get_project_git_config_url(dir_path)
        if x is None:
            pass
        else:
            self.repoLink = x

    def getRepoLink():
        return self.repoLink

    def get_project_git_config_url(self, directory):
        git_config_path = os.path.join(directory, '.git', 'config')
        if not os.path.exists(git_config_path):
            return None
            # raise FileNotFoundError(f"The .git/config file does not exist in the specified directory: {directory}")

        # Read the contents of the git config file
        with open(git_config_path, 'r', encoding='utf-8') as config_file:
            config_content = config_file.read()

        # Parse the config content using configparser
        config_parser = configparser.ConfigParser()
        config_parser.read_string(config_content)

        # Get the URL from the parsed config
        try:
            url = config_parser.get('remote "origin"', 'url')
            return url
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            return None
            # raise ValueError(f"Failed to retrieve URL from git config: {e}")

    def getName(self):
        return self.name

