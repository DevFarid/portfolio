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
        self.projects = [project(f) for f in Utilities.list_directories(dir_path)]

    def len(self):
        return len(self.projects)

    def getProjects(self):
        return self.projects

    def getProject(self, index):
        return self.projects[index]

    def getProjectName(self, index):
        return self.projects[index].getName()

    def getProjectIcon(self, index):
        return self.projects[index].getIcon()

    def getProjectByName(self, name):
        if self.hasProject(name):
            return next(p for p in self.projects if p.getName() == name)

    def hasProject(self, project_name):
        return any(p.getName() == project_name for p in self.projects)
    
    def getShortDescription(self, index):
        return self.projects[index].getShortDescription()

if __name__ == "__main__":
    x = project_loader()