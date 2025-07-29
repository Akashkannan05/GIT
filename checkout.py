import os
import zlib

from status import parse_tree_object
BASE_PATH=os.getcwd()
OBJECTS_DIR="GIT/objects"
FILES=[]

#Step1:input the  Commit Hash or Reference , Load the Commit Object and get tree hash
def load_commit_object(commit_hash=None):
    if commit_hash==None or len(commit_hash)!=64:
        # print(len(commit_hash))
        print("Enter the valid commit hash......")
        return
    folder_path=os.path.join(OBJECTS_DIR,commit_hash[:2])
    file_path=os.path.join(folder_path,commit_hash[2:])
    if not os.path.isfile(file_path):
        print("Enter the valid commit hash........|")
        return
    with open(file_path,"rb") as f:
        commpressed_content=f.read()
    content=zlib.decompress(commpressed_content).decode()
    # print(content)
    tree=content.split("\n")[0]
    tree_hash=tree.split()[-1]
    print(tree_hash)
    return tree_hash

#load_commit_object("a563cf5950844396e1649b6eca2560ee8e5c39ecc0bc90afbd66332b8c919c1d")

def load_tree_object(tree_hash):
    folder_path = os.path.join(OBJECTS_DIR, tree_hash[:2])
    file_path = os.path.join(folder_path, tree_hash[2:])
    if not os.path.isfile(file_path):
        print("Tree's file is not available.......")
        return
    with open(file_path, "rb") as f:
        compressed_content = f.read()
    content = zlib.decompress(compressed_content)
    # print(content)
    # print("LEN:",len(content))
    null_byte_index = content.find(b'\x00')
    body = content[null_byte_index + 1:]
    index = 0
    tree = []
    while index < len(body):
        mode = ""
        while chr(body[index]) != ' ':
            mode += chr(body[index])
            index += 1
        index += 1 
        fileName = ""
        while body[index] != 0:
            fileName += chr(body[index])
            index += 1
        index += 1  
        hash_bytes = body[index:index+32]
        hash_hex = hash_bytes.hex()
        index += 32
        tree.append({
            "mode": mode,
            "fileName": fileName,
            "hash": hash_hex
        })
    print(tree)
    return tree
    
# load_tree_object("a563cf5950844396e1649b6eca2560ee8e5c39ecc0bc90afbd66332b8c919c1d")

# Step 3: Recursively process tree entries and restore files/folders
def traverse_tree(tree_hash, path_prefix=""):
    entries = load_tree_object(tree_hash)
    if entries is None:
        return
    for entry in entries:
        mode = entry["mode"]
        name = entry["fileName"]
        sha = entry["hash"]
        full_path = os.path.join(BASE_PATH, path_prefix, name)
        
        if mode == "40000":  
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            traverse_tree(sha, os.path.join(path_prefix, name))
        else:
            restore_blob(sha, full_path)

# Step 4: Restore blob contents to file
def restore_blob(blob_hash, output_path):
    folder_path = os.path.join(OBJECTS_DIR, blob_hash[:2])
    file_path = os.path.join(folder_path, blob_hash[2:])
    if not os.path.isfile(file_path):
        print(f"Blob object not found.........")
        return
    with open(file_path, "rb") as f:
        compressed_content = f.read()
    content = zlib.decompress(compressed_content)
    null_byte_index = content.find(b'\x00')
    blob_content = content[null_byte_index + 1:]

    with open(output_path, "wb") as f:
        f.write(blob_content)
    print(f"Restored file: {output_path}")

# Step 5 (Optional): Clear current working directory before checkout
def clear_working_directory(exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = ['GIT']  # do not delete .git directory
    
    for item in os.listdir(BASE_PATH):
        if item in exclude_dirs:
            continue
        item_path = os.path.join(BASE_PATH, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            import shutil
            shutil.rmtree(item_path)

# Main checkout function
def checkout(commit_hash):
    clear_working_directory()

    tree_hash = load_commit_object(commit_hash)
    if tree_hash is None:
        print("Checkout failed: invalid commit hash.................")
        return

    traverse_tree(tree_hash)
    print("Checkout completed.")

checkout("a563cf5950844396e1649b6eca2560ee8e5c39ecc0bc90afbd66332b8c919c1d")