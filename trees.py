import os
import hashlib
import zlib

from blob import compute_SHA_256,compress_byte_data
OBJECTS_DIR="GIT/objects"


#<mode> <filename>\0<20-byte SHA-1 hash of object>
#sha256().digest() → a 32-byte raw binary value

#STEP 1:Traverse Folder
def traverse_folder(folder_path=None):
    if folder_path is None or not os.path.isdir(folder_path):
        print("Enter the proper folder name")
        return None
    # files_and_folers=os.listdir(folder_path)
    # print(files_and_folers)
    files=[]
    output=[]
    for file in os.listdir(folder_path):
        file_path=os.path.join(folder_path,file)
        if os.path.isfile(file_path):
            files.append(file_path)
            # print("---------------------------",file_path)
            compress_byte_data(file_path)
            dictioanry={
                "name":file_path.split('/')[-1],
                "type":"file",
                "hash":compute_SHA_256(file_path).hexdigest()
            }
            output.append(dictioanry)
    folders=[]
    for folder in os.listdir(folder_path):
        sub_folder_path=os.path.join(folder_path,folder)
        if os.path.isdir(sub_folder_path):
            folders.append(sub_folder_path)
            dictioanry={
                "name":sub_folder_path.split('/')[-1],
                "type":"tree",
                "hash":store_tree(sub_folder_path)
            }
            output.append(dictioanry)
    # print(files)
    # print(folders)
    
    # for file in files:
        
    # print(output)
    return output

#Step 2:Build Binary Tree Entries
def build_binary_tree_entries(folder_path=None):
    entries=traverse_folder(folder_path)
    tree_entries=[]
    for i in entries:
        if i.get('type')=="file":
            mode="100644"
        elif i.get('type')=="tree":
            mode="40000"
        else:
            print("Somethig wrong in assigning mode in build_binary_tree_entries()...........")
            return None
        header=f"{mode} {i.get('name')}\0"
        # print(header)
        header_byte=header.encode()
        tree_entery=header_byte + bytes.fromhex(i.get("hash"))
        tree_entries.append(tree_entery)
    return(tree_entries)

#Step 3:Add Tree Header
def add_tree_header(folder_path=None):
    tree_entries=build_binary_tree_entries(folder_path)
    if len(tree_entries)==0:
        print("The Tree entries is empty..............")
    tree_body=tree_entries[0]
    if(len(tree_entries)>1):
        for i in tree_entries[1:]:
            tree_body+=i
    tree_header=f"tree {len(tree_body)}\0"
    tree_header_byte=tree_header.encode()
    # print(tree_header_byte)
    tree_object=tree_header_byte+tree_body
    return tree_object

#Step 4:Hash and Compress
def hash_and_compress(folder_path=None):
    tree_object=add_tree_header(folder_path)
    if tree_object is None:
        print("something went wrong in the add_tree_header")
        return None
    hash_object=hashlib.sha256()
    hash_object.update(tree_object)
    hash=hash_object.hexdigest()
    compress=zlib.compress(tree_object)
    return hash,compress

#Step 5:Store Object
def store_tree(folder_path=None):
    hash_compress=hash_and_compress(folder_path)
    if hash_compress is None or len(hash_compress)!=2:
        print("Something went wrong in the hash_and_compress......")
        return None
    hash,compress=hash_compress
    folder=os.path.join(OBJECTS_DIR,hash[:2])
    os.makedirs(folder, exist_ok=True)
    file_path=os.path.join(folder,hash[2:])
    with open(file_path,"wb") as f:
        f.write(compress)
    print("CREATED")
    return hash
