import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import *

class learning_loader():
    def __init__(self):
        self.learnings = []
        self.load()

    def load(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.learnings = [learning(f) for f in os.listdir(dir_path) if not (f.startswith('__pycache__') or f.endswith(".py"))]

    def len(self):
        return len(self.learnings)
    
    def getLearnings(self):
        return self.learnings

    def getLearningName(self, index):
        return self.learnings[index].getName()
    
    def getLearning(self, index):
        return self.learnings[index]
    
    def hasLearning(self, learning_name):
        return any(l.getName() == learning_name for l in self.learnings)
    
    def getLearningByName(self, learning_name):
        for l in self.learnings:
            if l.getName() == learning_name:
                return l
        return None
    
    def getTree(self, index):
        return self.learnings[index].getTree()

    
class learning():
    def __init__(self, name):
        self.name = name
        self.fileTree = {}
        self.load()

    def load(self):
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.name)
        self.fileTree = Utilities.get_directory_tree(dir_path)

    def getTree(self):
        return self.fileTree

    def printTree(self):
        Utilities.print_tree(self.fileTree)

    def getName(self):
        return self.name
    


if __name__ == "__main__":
    x = learning_loader()
    print(x.getLearningName(0))
    print(x.getLearning(0).printTree())