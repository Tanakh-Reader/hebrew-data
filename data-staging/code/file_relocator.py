import os 
import shutil

class FileRelocator:

    def copy_to_new_dir(self, source_path:str, dest_path:str):

        shutil.copyfile(source_path, dest_path)

        return dest_path
