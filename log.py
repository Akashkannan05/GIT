import os

BASE_PATH=os.getcwd()
OBJECTS_DIR="GIT/objects"
HEAD_DIR=os.path.join(BASE_PATH,"GIT/HEAD")
#SETP 1:Read the Commit Hash from .vcs/HEAD
def read_head():
    if not os.path.exists(HEAD_DIR):
        print("There is no commit.............")
        return None
    with open(HEAD_DIR,"r") as f:
        head=f.read()
    commit_object_folder=os.path.join(BASE_PATH,head[:2])
    commit_object_path=os.path.join(commit_object_folder,head[2:])
    if not os.path.exists(commit_object_path):
        print("There is no path for this object ........")
        return None
    return commit_object_path

#Step 2:Load the Commit Object from .vcs/objects/
