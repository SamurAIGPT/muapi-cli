from .client import upload_file


class UploadsAPI:
    def upload(self, file_path: str):
        return upload_file(file_path)