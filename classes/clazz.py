import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import *

class class_loader():
    def __init__(self):
        self.classes = []
        self.load()

    def load(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.classes = [clazz(f) for f in Utilities.list_directories(dir_path)]

    def len(self):
        return len(self.classes)

    def getClassName(self, index):
        return self.classes[index].getName()

    def len_of_cproj(self, index):
        return self.classes[index].len()

    def clazz(self, index):
        return self.classes[index]

    def hasClass(self, clazz_name):
        return any(c.getName() == clazz_name for c in self.classes)

    def hasProject(self, clazz_name, project_name):
        return any(p.getName() == project_name for p in next(c for c in self.classes if c.getName() == clazz_name).getClassProjects())

    def getClassProject(self, project):
        for c in self.classes:
            for p in c.getClassProjects():
                if p.getName() == project:
                    return p
                
    def getProjectCount(self):
        return sum(c.len() for c in self.classes)
                    
class clazz:
    def __init__(self, name):
        self.name = name
        self.formal_name = None
        self.projects = []
        self.load()

    def load(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.name)
        self.projects = [project(f, self.name) for f in Utilities.list_directories(dir_path)]
        self.formal_name = Utilities.get_formal_name(dir_path)

    def getName(self):
        return self.name
    
    def getFormalName(self):
        return self.formal_name
        
    def len(self):
        return len(self.projects)

    def getClassProjects(self):
        return self.projects


if __name__ == "__main__":
    x = class_loader()