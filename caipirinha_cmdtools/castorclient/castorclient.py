import os
# import pandas as pd


class CastorClient(object):

    def __init__(self):
        self.current_dir = os.path.abspath(os.path.curdir)
        # self.data = None

    def print_current_dir(self):
        print(self.current_dir)

    # def pwd(self):
    #     return self.current_dir
    #
    # def cd(self, d):
    #     self.current_dir = os.path.join(self.current_dir, d)
    #     self.pwd()
    #
    # def ls(self):
    #     entries = []
    #     for f in os.listdir(self.current_dir):
    #         entries.append(f)
    #     return entries
    #
    # def load_excel(self, file_name):
    #     if os.path.isfile(file_name):
    #         file_path = file_name
    #     else:
    #         file_path = os.path.join(self.current_dir, file_name)
    #     self.data = pd.read_excel(file_path)
    #     return self.data
