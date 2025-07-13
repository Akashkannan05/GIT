import os
import time
import configparser
import hashlib
import zlib
from trees import store_tree


BASE_PATH=os.getcwd()
OBJECTS_DIR="GIT/objects"
HEAD_DIR=os.path.join(BASE_PATH,"GIT/HEAD")
VCSCONFIG_DIR=os.path.join(BASE_PATH,"GIT/.vcsconfig")

#STEP1: Get the Tree Hash
def get_tree_hash(folder_path=None):
    hash=store_tree(folder_path)
    tree_body=f"tree {hash}"
    return tree_body,hash

#STEP2:Get the Parent Commit Hash (Optional)
def parent_commit(folder_path=None):
    tree_body,hash=get_tree_hash(folder_path)
    if os.path.exists(HEAD_DIR):
        with open(HEAD_DIR,"r") as f:
            parent_hash=f"parent {f.read()}"
            # print(parent_hash)
    else:
        parent_hash="No parent"
    # print(HEAD_DIR)
    with open(HEAD_DIR,"w") as f:
        f.write(hash)
    return tree_body,parent_hash
    
#STEP3: Add Author and Committer Metadata
def add_author_committer_metadata():
    print("SSSẞ")
    #commit_body,parent_hash=parent_commit(folder_path)
    parser = configparser.ConfigParser()
    parser.read(VCSCONFIG_DIR)
    author_info,commiter_info=parser["author"],parser["committer"]
    print(".................",author_info)
    if author_info.get("name") is None or author_info.get("email") is None:
        print("Author details is not filled.........")
        return None
    author=f"author {author_info.get('name')} {author_info.get('email')} {int(time.time())} {time.strftime('%z')}" #{time.strftime('%z')}=>Local time
    if commiter_info.get("name") is None or commiter_info.get("email") is None:
        print("Commiter details is not filled.........")
        return None
    commiter=f"author {commiter_info.get('name')} {commiter_info.get('email')} {int(time.time())} {time.strftime('%z')}" #{time.strftime('%z')}=>Local time
    return author,commiter

#STEP4:Combine All Components (Commit Body)
def body(folder_path=None,commit_msg=None):
    if commit_msg is None or commit_msg.strip()=="":
        print("Commit msg cant me empty string or None........")
        return
    tree_body,parent_hash=parent_commit(folder_path)
    if tree_body is None or parent_hash is None:
        print("Somethig went wrong in parent_commit...............")
        return None
    author,commiter=add_author_committer_metadata()
    if author is None or commiter is None:
        print("Something went wrong in add_author_committer_metadata...........")
        return None
    if parent_hash!="No parent":
        body=f"""
            {tree_body}
            {parent_hash}
            {author}
            {commiter}
            \n
            {commit_msg}
            """
    else:
        body=f"""
            {tree_body}
            {author}
            {commiter}
            \n
            {commit_msg}
            """
    print( body)
    return body

def hash_compree_build(folder_path=None,commit_msg=None):
    commit_body=body(folder_path=folder_path,commit_msg=commit_msg)
    if commit_body is None:
        print('somthing went wrong in the body()................')
        return None
    commit_body_byte=commit_body.encode()
    commit_header=f"commit {len(commit_body)}\0"
    commit_header_byte=commit_header.encode()
    commit=commit_header_byte+commit_body_byte
    hash_object=hashlib.sha256()
    hash_object.update(commit)
    commit_hash=hash_object.hexdigest()
    commit_compress=zlib.compress(commit)

    folder_path=os.path.join(OBJECTS_DIR,commit_hash[:2])
    os.makedirs(folder_path, exist_ok=True)
    file_path=os.path.join(folder_path,commit_hash[2:])
    with open(file_path,"wb") as f:
        f.write(commit_compress)
    print(f"The commit file is created at {file_path}")
