from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadedfile import TemporaryUploadedFile

class TemporaryFileUploadHandler_2(FileUploadHandler):
    """
    Upload handler that streams data into a temporary file.
    """
    def __init__(self, *args, **kwargs):
        super(TemporaryFileUploadHandler_2, self).__init__(*args, **kwargs)
        print("hello")
    def new_file(self, *args, **kwargs):
        """
        Create the file object to append to as data is coming in.
        """
        super(TemporaryFileUploadHandler_2, self).new_file(*args, **kwargs)
        self.file = TemporaryUploadedFile(self.file_name, self.content_type, 0, self.charset, self.content_type_extra)

    def receive_data_chunk(self, raw_data, start):
        self.file.write(raw_data)

    def file_complete(self, file_size):
        self.file.seek(0)
        self.file.size = file_size
        return self.file
