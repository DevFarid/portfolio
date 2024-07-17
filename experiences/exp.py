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
        self.experiences = [experience(f) for f in os.listdir(dir_path) if not (f.startswith('__pycache__') or f.endswith(".py"))]

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

class experience:
    def __init__(self, name):
        self.name = name
        self.jobFunctions = []

    def getName(self):
        return self.name

if __name__ == "__main__":
    x = experience_loader()