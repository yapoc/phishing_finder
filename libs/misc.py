import os
def get_file_full_path (relative_file_path, relative_from = ""):
    return os.path.abspath("{}/{}".format (os.path.dirname(relative_from), relative_file_path))
