from controllers.BaseController import BaseController
from controllers.ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal

import re , os

class DataController(BaseController):


    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_uplodes(self, file : UploadFile):

         if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
             return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
         
         if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
             return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
         
         return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value
    

    def generate_filepath(self, filename:str, project_id):
        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        clean_filename = self.get_clean_filename(filename=filename)
        new_filename = os.path.join(
            project_path, random_filename+"_"+ clean_filename
        )

        while os.path.exists(new_filename):
            random_filename= self.generate_random_string()
            new_filename = os.path.join(
            project_path, random_filename+"_"+ clean_filename
        )
            
        return new_filename , random_filename+"_"+ clean_filename


    def get_clean_filename(self, filename :str):
        clean_name = re.sub(r'[^\w.]','',filename.strip())
        clean_name = clean_name.replace(" ","_")
        return clean_name
