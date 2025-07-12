import os
import hashlib
import zlib
#BLOB => Binary Large Object


BASE_DIR = 'documents'
OBJECTS_DIR="objects"

file_content=None

#STEP1:Git reads the entire file as a byte stream (raw bytes).
def read_document_convert_to_byte_stream(actual_file_path=None):
    if actual_file_path is None:
        print("provide the file path")
        return None
    # if  not os.path.isdir(actual_file_path):
    #     print("There is no documnet with this id")
    #     return None
    # print("--------------------------->>>>>>>>>",actual_file_path)
    with open(actual_file_path,"r") as f:
        global file_content
        file_content=f.read()
    # print(file_content)
    return file_content.encode()

#STEP2:Git constructs a byte stream: b"blob <size>\0<file-content>"
# def create_blob_object(doc_id,version):
def create_blob_object(actual_file_path=None):
    file_content_byte_stream=read_document_convert_to_byte_stream(actual_file_path)
    if file_content_byte_stream is None:
        print("Something went wrong in read_document_convert_to_byte_stream.....")
        return None
    if file_content is None:
        print("Something went wrong in read_document_convert_to_byte_stream.....")
        return None
    header=f"blob {len(file_content)}\0"
    header_byte=header.encode()
    blob=header_byte+file_content_byte_stream
    return blob

#STEP3:Compute SHA-256 Hash
def compute_SHA_256(actual_file_path=None):
    blob=create_blob_object(actual_file_path)
    if not blob :
        print("Something went wrong in create_blob_object.....")
        return None
    hash_obj=hashlib.sha256()
    hash_obj.update(blob)
    # print(hash_obj.hexdigest())
    return hash_obj

#STEP4:Compress the Blob Object and Store the Compressed Object
def compress_byte_data(actual_file_path=None):
    blob=create_blob_object(actual_file_path)
    if not blob :
        print("Something went wrong in create_blob_object.....")
        return None
    compress_data=zlib.compress(blob)
    #original = zlib.decompress(compress_data) byte data
    hash=compute_SHA_256(actual_file_path).hexdigest()
    if hash is None:
        print("Something went wrong in compute_SHA_256.....")
        return None
    folder_name=hash[0:2]
    file_name=hash[2:]
    folder_path=os.path.join(OBJECTS_DIR,folder_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path=os.path.join(folder_path,file_name)
    with open(file_path,"wb") as f:
        f.write(compress_data)
    print(f"The compressed file is created at {file_path}")