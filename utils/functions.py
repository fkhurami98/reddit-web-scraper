import os


class CurrentPath:
    def __init__(self, caller_file):
        self.current_directory = os.path.dirname(os.path.abspath(caller_file))
        self.save_path = os.path.join(self.current_directory, "json_data_folder")

    def get_save_path(self):
        return self.save_path
