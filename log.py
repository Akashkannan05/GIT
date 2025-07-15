import os
import zlib 
import hashlib
import time

BASE_PATH=os.getcwd()
OBJECTS_DIR="GIT/objects"
HEAD_DIR=os.path.join(BASE_PATH,"GIT/HEAD")
commit_path = None
#SETP 1:Read the Commit Hash from .vcs/HEAD
def read_head():
    if not os.path.exists(HEAD_DIR):
        print("There is no commit.............")
        return None
    with open(HEAD_DIR,"r") as f:
        head=f.read()
    return head

def commit_path_finder(commit_hash=None):
    if commit_hash is None:
        print("please provide commit hash...........")
    commit_object_folder=os.path.join(OBJECTS_DIR,commit_hash[:2])
    commit_object_path=os.path.join(commit_object_folder,commit_hash[2:])
    if not os.path.exists(commit_object_path):
        print(f"There is no path for this object ........{commit_object_path}")
        return None
    return commit_object_path

#Step 2:Load the Commit Object from .vcs/objects/
#GIT/objects/e3/97e3f061c9b95a0c082c87dc41b72432e00052f2d05ab5ba081d9e6259053e

def load_commit_object(commit_path=None):
    # commit_path = read_head()
    if commit_path is None:
        print("Commit cant be None make sure you atleast have on commit")
    with open(commit_path, "rb") as f:
        commit_content_compress = f.read()
    commit_content = zlib.decompress(commit_content_compress)
    # print(commit_content)
    null_index = commit_content.find(b'\x00')
    header = commit_content[:null_index].decode('utf-8') 
    body = commit_content[null_index + 1:]
    if header.startswith("commit"):
        print("****commit****\n")
        # print(body.decode("utf-8")) 
        return body.decode("utf-8") 
    #there are hash objects in the tree body
    else:
        print("TREE:",body)
        #TREE: b'100644 hello.txt\x00\xcc5r{\xab\xcaOV\x84\x9e\x1f\xe6\x1a\x8b\xbe\xfa\xd8/\xfdm-\xd5\xfb \x92q\xfef\xcb;\xf7{40000 doc_Document1\x00n,K\xe0\x8e\x95\xb8N\xeb\x83\xe0+:\xa7\xf2]):\xdcs\xa3\xb7SX`\xd0\xbf>r\xf3\xbc\xf7'
        index=0
        tree=[]
        while index!=len(body):
            mode=""
            for i in body[index:]:
                if chr(i)==" ":
                    index+=1
                    break
                print("=============>",chr(i))
                mode+=chr(i)
                index+=1
            null_byte_index=body.find(b'\x00',index)
            # if(c==1):
            #     print(null_byte_index)
            #     break
            if null_byte_index==-1:
                print("SOmething went wrong................")
                break
            fileName=""
            while (index!=null_byte_index):
                fileName+=chr(body[index])
                index+=1
            index+=1
            print("???????????",body[index:index+32])
            hash=(body[index:index+32]).hex()
            tree.append({
                "mode":mode,
                "fileName":fileName,
                "hash":hash
            })
            index=index+32
            print(tree)

def print_commit():
    global commit_path
    if commit_path is None:
        commit_hash=read_head()
        # print("*************************",commit_path)
        commit_path=commit_path_finder(commit_hash)
    #     print("*************************",commit_path)
    #     print("AKASH-1ST COMMIT")
    # print("*************************",commit_path)
    commit_body=load_commit_object(commit_path)
    # commit 255tree e41ca631392626f4832f4da1bf94690121d7465d00c3cc5637d6e687fb2e0dff
    # parent 6bf2c7b8e802d2dd677fe2dfa47c177f904da6d4b75d96fab47a31893b90b6e5
    # author Akash akash@example.com 1752540008 +0530
    # commiter Akash akash@example.com 1752540008 +0530
    #
    #1st commit msg
    commit_body=commit_body.split('\n')
    commit_hash=f"commit {commit_path.split('/')[-1]+commit_path.split('/')[-2]}"
    author_list=commit_body[-4].split()
    author=f"Author :{author_list[1]} {author_list[2]}"
    timestamp=int(author_list[-2])
    print("*********",timestamp)
    print("*********",type(timestamp))
    date=f"Date : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((timestamp)))} {author_list[-1]}"
    commit_msg=commit_body[-1]
    print(f"""
        {commit_hash}
        {author}
        {date}

        {commit_msg}
          """)
    print("---------------------")
    if commit_body[1].startswith('parent'):
        commit_hash=commit_body[1].split()[-1]
        commit_path=commit_path_finder(commit_hash)
        print_commit()
    
