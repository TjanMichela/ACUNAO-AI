
# ACUNAO AI

## Folder Description  

This folder contains the Jupyter Notebooks used for experimentation and testing purposes. Start with the `dev.ipynb` file. Naming convention for new notebooks should reflect the main changes in the notebook. For example: `add-multiquery-retriever.ipynb`.  

## Table of Contents

* [Installation](#installation)
* [Project History](#project-history)
* [Maintainers](#maintainers)
    * [Contributors](#contributors)
* [License](#license)

## Installation

To set up ACUNAO AI locally, follow these steps in your terminal, PowerShell, or CommandPrompt:  

1. **Clone the repository** or **Download the repository**  
```bash
git clone https://github.com/luquelab/ACUNAO.git
```  
2. **Navigate to project directory**  
```bash
cd ACUNAO
```  
  or 
```bash
cd ACUNAO-main
```
  Note: if you are new to the terminal, PowerShell or CommandPrompt, run `ls` to see the current directory and `cd` to navigate to the ACUNAO folder.  

3. **Create a virtual environment**  
  Note: In MacOS, make sure that Xcode is installed. To do this, run this command in your terminal:
```
xcode-select –-install
```
```bash
python3 -m venv venv
```
4. **Activate the virtual environment**

  4.1. For macOS and Linux: 
```
source venv/bin/activate
```

  4.2. For Windows: 
```
venv\Scripts\activate
```
or 
```
.\venv\Scripts\Activate.ps1
```
If it doesn't work on Windows PowerShell, run the following code before activating the environment using the code above: 
```
set-executionpolicy RemoteSigned
```

5. **Install dependencies**  

  5.1. For Mac:  
This project requires Tesseract to be installed on your system. You can install Tesseract using Homebrew with the following command:
```bash
brew install tesseract
```
Then:
```bash
pip install -r src/requirements.txt
```  

  5.2. For Windows:  
1. Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.
2. Install this exe in `C:\Program Files (x86)\Tesseract-OCR`

  Then: 
```bash
pip install -r src/requirements.txt
```

6. **Install the LLM**  
Download Ollama from the following link: https://ollama.com/
Then open the app, install Ollama, and keep Ollama open.  

7. **You're Now Ready to Use the Jupyter Notebook!**  


## Project History

This is an evolving repository  

Started: 2024-06-03

End: Ongoing


## Maintainers

[@LuqueLab](https://github.com/luquelab)

### Contributors

This project exists thanks to all the people who contribute.  
[@LuqueLab](https://github.com/luquelab)

## License

This project is licensed under a license.

------
The syntax of markdown files (.md) is CommonMark unless specified otherwise (https://commonmark.org/help/)
