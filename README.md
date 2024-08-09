
# ACUNAO AI

## Description

An AI assistant as a domain expert of the lab’s documents that has the ability to answer users’ queries accurately. The user must be able to trust the answers given by the AI assistant and give input in order for the AI assistant to continuously learn how to better respond to users’ queries. 

Due to the rapid growth of AI, especially since the launch of ChatGPT, there has been a drastic increase in AI products and services. These products and services have mostly been developed to appeal to the general public. There is a lack of AI solution to support interdisciplinary research labs whose documents could accumulate so quickly, which leads to misplaced or forgotten information. The nature of these documents also poses as a problem since they are generally complex and confidential. ACUNAO aims to bridge this gap.

## Table of Contents

* [Installation](#installation)
* [Documentation](#documentation)
* [Project History](#project-history)
* [Folder's descriptions](#folders-descriptions)
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
For Conda users, skip to step 5.  

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

  5.1.1. For Conda Users:   

```
conda create --name venv --file requirements.txt
```
```
conda activate venv
```
```
conda install -c conda-forge tesseract
```

  5.1.2. For Conda Users: (Alternative)  

```
conda env create --name venv --file=environments.yml
```
```
conda activate venv
```

  5.2. For Mac:  
This project requires Tesseract to be installed on your system. You can install Tesseract using Homebrew with the following command:
```bash
brew install tesseract
```
Then:
```bash
pip install -r requirements.txt
```  

  5.3. For Windows:  

If you are a Conda user, use the following commands:  
```
conda create --name venv --file src/requirements.txt
```
Then:  
```
conda activate venv
```
```
conda install -c conda-forge tesseract
```

  5.2. For Windows:  
  
1. Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki  
2. Install this exe in `C:\Program Files (x86)\Tesseract-OCR`   

  Then: 
```bash
pip install -r requirements.txt
```

6. **Install the LLM**  

Download Ollama from the following link: https://ollama.com/    

Then open the app, install Ollama, and keep Ollama open.   

7. **Run the application**  

  7.1. Run the Streamlit prototype:  
```bash
streamlit run src/app.py
```
  
  7.2. Run the dev Jupyter Notebook:  
  Navigate to the `dev.ipynb` file within the dev folder.   

## Documentation

ACUNAO's documentation is available as a GitHub-pages website accessible at [add later]. The documentation's source files are located in this repository at https://github.com/luquelab/ACUNAO/tree/main/docs.

## Project History

This is an evolving repository  

Started: 2024-06-03

End: Ongoing

## Folder's descriptions

* `/data`: Files used for testing purposes.
* `/dev`: Jupyter Notebooks used for experimentation and testing. 
* `/docs`: This folder contains the project's documentation.
* `/src`: Project's source codes.

## Maintainers

[@LuqueLab](https://github.com/luquelab)

### Contributors

This project exists thanks to all the people who contribute.  
[@LuqueLab](https://github.com/luquelab)

## License

This project is licensed under a license.

------
The syntax of markdown files (.md) is CommonMark unless specified otherwise (https://commonmark.org/help/)
