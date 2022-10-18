import os 
import shutil
import zipfile


class FileRelocator:

    def copy_to_new_dir(self, source_path:str, dest_path:str):

        shutil.copyfile(source_path, dest_path)

        return dest_path


    def unzip_to_new_dir(self, source_path:str, dest_path:str):

        garbage_data = '__MACOSX'
        dest_dir = os.path.dirname(dest_path)
        source_file = os.path.basename(source_path)
        write_file = os.path.basename(dest_path)

        with zipfile.ZipFile(source_path, 'r') as zip_data:

            zip_infos = zip_data.infolist()
            # iterate through each file
            for zip_info in zip_infos:
       
                zip_info.filename = write_file if zip_info.filename == source_file else zip_info.filename
                zip_data.extract(zip_info, path=dest_dir)
                
        if garbage_data in os.listdir(dest_dir):
            os.rmdir(os.path.join(dest_dir, garbage_data))
        
        return dest_path