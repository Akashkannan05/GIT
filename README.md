# 🌀 Mini Git - Custom Version Control System in Python

This is a simplified Git-like version control system implemented in Python. It mimics basic Git functionality such as object storage, staging, committing, logging, status checking, and checkout operations.

## 🚀 Features

- **Blob Object Creation:**  
  Store file content as compressed objects using SHA-256 hashing.

- **Staging Area (`add`):**  
  Stage specific files or folders for commit, supporting recursive directory traversal.

- **Commit System:**  
  Save the current staged state with metadata like parent commit and commit message.

- **Tree Object Storage:**  
  Efficiently store directory structures with references to blobs and subtrees.

- **Log History (`log`):**  
  View the list of commits, showing commit hash, message, and timestamp.

- **Status (`status`):**  
  Compare working directory with last commit and show staged/unstaged changes.

- **Checkout (`checkout`):**  
  Restore the full file tree of a given commit hash into the working directory.

- **SHA-256 Object Directory:**  
  All objects (blobs, trees, commits) are stored under `GIT/objects` using the first two characters of their hash as subfolders (like Git).

## 🗂️ Directory Structure

project-root/
│
├── GIT/
│ ├── objects/ # Stores blob/tree/commit objects
│ ├── HEAD # Stores current HEAD commit hash
│ └── index # Staging area (list of staged files)
│
├── add.py # Script to stage files
├── commit.py # Script to commit changes
├── log.py # Script to view commit logs
├── status.py # Script to show status
├── checkout.py # Script to switch to a previous commit
├── blob.py # Contains functions for hashing and storing blob data
└── README.md # This file

## 🛠️ Technologies Used

- **Python 3.x**
- `zlib` for compression (like Git)
- `hashlib` for SHA-256 hashing
- Custom object parsing and file/directory handling

## 📌 Limitations

- No branch support
- No remote repository
- No conflict handling or merge support
- Only basic error handling

## 📚 Learning Outcomes

This project was built for learning:

- How Git internally stores data (blobs, trees, commits)
- How a Version Control System (VCS) works at a low level
- Hash-based object storage and traversal
- Recursive directory handling and compression

---

> 🧠 Built with ❤️ to understand the internals of Git by re-implementing it from scratch.

## 📬 Contact Me

Feel free to reach out if you have any questions or suggestions:

📧 [akash2005k26kaniyur12@gmail.com](mailto:akash2005k26kaniyur12@gmail.com)


>NOTE:The README.md file and few steps in checkout.py was created by the chatgpt not any other that is also due to lack of time
