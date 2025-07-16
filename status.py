import os
import zlib
import rich

from blob import compute_SHA_256

BASE_PATH=os.getcwd()
DOCUMENT_DIR = 'documents'
OBJECTS_DIR="GIT/objects"
HEAD_DIR=os.path.join(BASE_PATH,"GIT/HEAD")

#Step 1: Load Latest Commit's Tree
def load_latest_commits_tree():
    if not os.path.exists(HEAD_DIR):
        print("There is no commit yet.........")
        return None
    with open(HEAD_DIR,"r") as f:
        commit_hash=f.read()
    commit_folder=os.path.join(OBJECTS_DIR,commit_hash[:2])
    commit_file=os.path.join(commit_folder,commit_hash[2:])
    with open(commit_file,"rb") as f:
        commit_content=f.read()
    # print(commit_content.decode())
    commit_content=zlib.decompress(commit_content)
    commit=""
    for i in commit_content:
        commit+=chr(i)
    # print(commit)
    tree_hash=commit.split('\n')[0].split()[-1]
    # print(tree_hash)
    tree_folder=os.path.join(OBJECTS_DIR,tree_hash[:2])
    tree_file=os.path.join(tree_folder,tree_hash[2:])
    # print(tree_file)
    with open(tree_file,"rb") as f:
        tree_content=f.read()
    tree_content=zlib.decompress(tree_content)
    null_index = tree_content.find(b'\x00')
    header = tree_content[:null_index].decode('utf-8') 
    body = tree_content[null_index + 1:]
    # tree=""
    # for i in tree_content:
    #     tree+=chr(i)
    # print(header)
    # print(body)
    index=0
    tree=[]
    while index!=len(body):
        mode=""
        for i in body[index:]:
            if chr(i)==" ":
                index+=1
                break
            # print("=============>",chr(i))
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
        # print("???????????",body[index:index+32])
        hash=(body[index:index+32]).hex()
        tree.append({
            "mode":mode,
            "fileName":fileName,
            "hash":hash
        })
        index=index+32
    # print(tree)
    # return tree
    # print(tree)
    for i in tree:
        if i["mode"]=="40000":
            # print("-------->",i)
            folder_path=os.path.join(DOCUMENT_DIR,i["fileName"])
            # print(";;;;;;;;;;;;;;;;;;;;;",folder_path)
            tree.extend(scan_the_working_directory(folder_path))
            tree.remove(i)
    # print("TREE:",tree)
    return tree


#Step 2: Scan the Working Directory
def scan_the_working_directory(folder_path=None, relative_path=""):
    if folder_path is None or not os.path.exists(folder_path):
        print("Give the proper directory")
        return None
    # print("@@@@@@@@@@@@",folder_path)
    files=os.listdir(folder_path)
    current_files=[]
    # print("==============>",files,folder_path)
    # print(files)
    for file_name in files:
        # print("FILE_NAME:",file_name)
        full_path = os.path.join(folder_path, file_name)
        rel_path = os.path.join(relative_path, file_name)
        # print("FILE_PATH:",file_path)
        if os.path.isfile(full_path):
            dictionary={
                'mode':'100644',
                'fileName':rel_path,
                'hash':compute_SHA_256(full_path).hexdigest()
            }
            current_files.append(dictionary)
        elif os.path.isdir(full_path):
            current_files.extend(scan_the_working_directory(full_path, rel_path))
    # print("CURRENT_FILES@:",current_files)
    return current_files
# Step 3: Compare Current State vs Commit Snapshot
def compare(folder_path=None):
    # print(current_files)
    latest_commit=load_latest_commits_tree()
    current_files=scan_the_working_directory(folder_path)
    print("LATEST_COMMIT:",latest_commit,"\n")
    print("CURRENT_FILES:",current_files,'\n')
    file_names=[]
    for dictionary in latest_commit:
        file_names.append(dictionary['fileName'])
    
    current_file_names = []
    for dictionary in current_files:
        current_file_names.append(dictionary['fileName'])

    new_added=[]
    for current_file_dictionary in current_files:
        if current_file_dictionary['fileName'] not in file_names:
            new_added.append(current_file_dictionary['fileName'])

    deleted = []
    for old_file_dictionary in latest_commit:
        if old_file_dictionary['fileName'] not in current_file_names:
            deleted.append(old_file_dictionary['fileName'])
            
    modified=[]
    not_changed=[]
    for current_file_dictionary in current_files:
        if current_file_dictionary['fileName'] not in new_added:
            for dictionary in latest_commit:
                if current_file_dictionary['fileName']==dictionary['fileName']:
                    if current_file_dictionary['hash']!=dictionary['hash']:
                        modified.append(current_file_dictionary['fileName'])
                    else:
                        not_changed.append(current_file_dictionary['fileName'])
                    # if current_file_dictionary in current_files:
                    current_files.remove(current_file_dictionary)
                    latest_commit.remove(dictionary)
    # modified=["hello"]
    if modified==[]:
        print("all Changes not staged for commit:")
    else:
        rich.print("[yellow]Changes not staged for commit:[/yellow]")
        for i in modified:
            rich.print(f"[yellow]{i}[/yellow]")
    # new_added=["hello"]
    if new_added==[]:
        print("No new files added")
    else:
        rich.print("[green]Files newly added[/green]")
        for i in new_added:
            rich.print(f"[green]{i}[/green]")
    # deleted=["hello"]
    if deleted==[]:
        print("No files deleted")
    else:
        rich.print("[red]deleted file[/red]")
        for i in deleted:
            rich.print(f"[red]{i}[/red]")