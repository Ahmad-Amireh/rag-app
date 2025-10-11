from .base_controller import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .project_controller import ProjectController
import re
import os

class DataController (BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_upload_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value


    def generate_unique_filepath(self, org_filename: str, project_id: str ):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_filename(org_filename=org_filename)
        new_file_path = os.path.join(project_path, random_key + "_" + cleaned_file_name)
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, random_key + "_" + cleaned_file_name)
        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_filename(self, org_filename: str):
        # Strip leading/trailing whitespace
        cleaned_file_name = org_filename.strip()

        # Replace spaces with underscores
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        # Remove all characters except word characters, dot (.) and underscore (_)
        cleaned_file_name = re.sub(r'[^\w._]', '', cleaned_file_name)

        return cleaned_file_name