import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import *

class experience_loader():
    def __init__(self):
        self.experiences = []
        self.load()

    def load(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.experiences = [experience(f) for f in Utilities.list_directories(dir_path)]

    def len(self):
        return len(self.experiences)
    
    def getExperiences(self):
        return self.experiences
    
    def getExperience(self, index):
        return self.experiences[index]
    
    def getExperienceName(self, index):
        return self.experiences[index].getName()
    
    def getExperienceByName(self, name):
        if self.hasExperience(name):
            return next(e for e in self.experiences if e.getName() == name)
    
    def hasExperience(self, experience_name):
        return any(e.getName() == experience_name for e in self.experiences)
    
    def getExperienceTitle(self, index):
        return self.experiences[index].getTitle()
    
    def getExperienceJobFunctions(self, index):
        return self.experiences[index].getJobFunctions()
    
    def getExperienceDate(self, index):
        return self.experiences[index].getDate()
    


class experience:
    def __init__(self, name):
        self.name = name
        self.title = None
        self.date = None
        self.jobFunctions = []
        self.load()

    def load(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.name)
        config = Utilities.read_experience_config(dir_path)
        if config is not None:
            self.title = config[0]
            self.date = config[1]
            self.jobFunctions = config[2]

    def getName(self):
        return self.name
    
    def getTitle(self):
        return self.title

    def getDate(self):
        return self.date

    def getJobFunctions(self):
        return self.jobFunctions
    
    def getJobFunction(self, index):
        return self.jobFunctions[index]
    
    def len(self):
        return len(self.jobFunctions)

if __name__ == "__main__":
    x = experience_loader()