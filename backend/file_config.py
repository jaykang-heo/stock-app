class FileConfig:
    _uploaded_file_path = ""

    @classmethod
    def get_uploaded_file_path(cls):
        return cls._uploaded_file_path

    @classmethod
    def set_uploaded_file_path(cls, path: str):
        cls._uploaded_file_path = path
