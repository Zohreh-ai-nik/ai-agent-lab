#this file has one job save the uploaded file into i atemporary location on disk, so the agent can read it and dlete it after we are done
import os
import tempfile


def save_uploaded_file(uploaded_file, suffix=".jpg"):
    """
    Streamlit gives us an uploaded file object.
    The agent needs a real file path on disk.
    So we save it to a temporary file and return the path.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getvalue())
    tmp.close()
    return tmp.name  # this is the full path like /tmp/tmpXYZ.jpg

def delete_file(path):
    """
    After the agent is done, we delete the temp file
    so we don't leave junk files on disk.
    """
    if os.path.exists(path):
        os.remove(path)
        
        
if __name__ == "__main__":
    
     # pretend we have a fake file and test save + delete
     # pretend we have a fake file and test save + delete
    path = "/tmp/test_utils_output.txt"
    
    with open(path, "w") as f:
        f.write("test")
    
    delete_file(path)
    print("delete_file works — file is gone:", not os.path.exists(path))
    # print("utils.py loaded successfully")
    # print("save_uploaded_file and delete_file are ready")