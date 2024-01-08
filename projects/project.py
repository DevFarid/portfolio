import os

class project_loader:

    def __init__(self):
        self.projects = []
        self.load()

    def load(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.projects = [folder for folder in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, folder))]

        
class project:

    def __init__(self, name):
        self.name = name



if __name__ == "__main__":
    x = project_loader()