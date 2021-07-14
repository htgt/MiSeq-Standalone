import os
import re


class DiscoverFolders():
    def get_dirs(self, folder_path):
        folders = os.listdir(folder_path)

        data = {
            'folder_path': folder_path,
            'basename' :  os.path.basename(folder_path),
            'folder_list' : folders,
        }

        return data