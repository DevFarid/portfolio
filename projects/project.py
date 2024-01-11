import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import *

class project_loader():

    def __init__(self):
        self.projects = []
        self.load()

    def load(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.projects = [project(f) for f in os.listdir(dir_path) if not (f.startswith('__pycache__') or f.endswith(".py"))]

    def len(self):
        return len(self.projects)

    def getProjects(self):
        return self.projects

    def getProjectName(self, index):
        return self.projects[index].getName()

    def hasProject(self, project_name):
        return any(p.getName() == project_name for p in self.projects)


if __name__ == "__main__":
    x = project_loader()