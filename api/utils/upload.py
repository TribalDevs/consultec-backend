import uuid
import os

def get_file_path(instance, filename):
    """
    This function is used to return a UUID for the file name 
    --> Returns the path for the file as {Classname}/{UUID}/
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(f'{instance.__class__.__name__}/', filename)