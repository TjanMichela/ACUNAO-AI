---
layout: default
title: Installation
nav_order: 2
---
# Get Started with ACUNAO-AI

## Download Instructions

Click <a href="{{ '/download/' | relative_url }}">**HERE**</a> to download ACUNAO-AI!

1. Download both files from the <a href="{{ '/download/' | relative_url }}">download link</a>:  
   - `ACUNAO-AI.zip`  
   - `ACUNAO-AI-README.txt`  
2. Keep the `ACUNAO-AI-README.txt` file for reference during setup or troubleshooting.


## First-Time Setup on macOS

To install and launch ACUNAO-AI on macOS:

1. Locate the downloaded `ACUNAO-AI.zip` file and unzip it.
2. Move the `ACUNAO-AI.app` file into your **Applications** folder.
3. Double-click on the `ACUNAO-AI.app` to open it.
4. You will see a message:  
   **"macOS cannot verify the developer of ACUNAO-AI."**  
   Click **Open**.
5. A second pop-up will appear with options: **Move to Trash** or **Close**.  
   Click **Close**.
6. Open **System Settings** on your Mac.
7. Navigate to **Privacy & Security**.
8. Scroll down to the **Security** section.
9. Under the message:  
   **'"ACUNAO-AI" was blocked from use because it is not from an identified developer'**,  
   click **Open Anyway**.
10. Reopen `ACUNAO-AI.app`.

> ⚠️ **Note:** The first launch might take some time as ACUNAO-AI completes initialization.


## Important Notice

Once ACUNAO-AI is launched, it will automatically create a folder named `ACUNAO-AI-Data` inside your **Documents** directory. This folder contains essential files and a sample project folder called `project_example`.

> 🚫 **Do NOT delete** the `ACUNAO-AI-Data` or `project_example` folders. These are critical for application functionality.


## General Usage Information

ACUNAO-AI is designed to answer questions based on the documents you provide. It **does not retain memory** of previous conversations or answers.

### Key Behaviors:
- It will notify you when a document is **processing** and when it is **ready**.
- It **cannot** respond to questions about documents that haven't been processed.
- When requesting a summary, **mention the document title** (as it appears in your project folder), not general terms like *"this paper"* or *"this document"*.
- ACUNAO-AI does **not** currently understand references like *"these documents"*, *"these PDFs"*, or *"this folder of files"*.


## Recommendations

Start by adding PDF files into the `ACUNAO-AI-Data` folder inside your **Documents** folder. Alternatively, click the **'Open ACUNAO-AI-Data Folder'** button from within the app's sidebar.

### Steps to Create a New Project:
1. Open the `ACUNAO-AI-Data` folder.
2. Create a new subfolder with your **project name**.
3. Add supported **PDF documents** into this folder. ACUNAO-AI will automatically process them.

### Data Management:
- Processed documents are tracked in a `metadata.json` file within each project folder.
- A `vectordb` folder stores your searchable embeddings.

> ⚠️ **Do NOT delete** `metadata.json` or `vectordb`.

### Pro Tip:
Organize complex projects by creating nested folders within your project folder—each acts as a separate topic-specific database!

### Sharing Projects:
You can share your project databases with others by copying and transferring the project folder.  
To load a shared project, simply move the folder into your own `ACUNAO-AI-Data` directory.


## Maintainers

- [@LuqueLab](https://github.com/luquelab)  
- [@TjanMichela](https://github.com/tjanmichela)

### Contributors

This project exists thanks to the continued efforts of our contributors:  
- [@LuqueLab](https://github.com/luquelab)  
- [@TjanMichela](https://github.com/tjanmichela)


## License

This project is licensed under the **MIT License**.