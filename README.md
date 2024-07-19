
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
To set up ACUNAO AI locally, follow these steps:

1. **Clone the repository**
```
git clone https://github.com/luquelab/ACUNAO.git
```
2. **Navigate to project directory**
```
cd ACUNAO
```
3. **Create a virtual environment**
```
python3 -m venv venv
```
4. **Activate the virtual environment**

For macOS and Linux:
```
source venv/bin/activate
```

For Windows:

Command Prompt
```
venv\Scripts\activate
```
PowerShell
```
.\venv\Scripts\Activate.ps1
```
5. **Install dependencies**
```
pip install -r requirements.txt
```
6. **Run the application**
```
streamlit run src/app.py
```

## Documentation
ACUNAO's documentation is available as a GitHub-pages website accessible at [add later]. The documentation's source files are located in this repository at https://github.com/luquelab/ACUNAO/tree/main/docs.

## Project History
This is an evolving repository
Started: 2024-06-03

End: Ongoing

## Folder's descriptions
* `/data`: Files used for testing purposes.
* `/docs`: This folder contains the project's documentation.
* `/results`: This folder contains the results, performance analysis, and commented references associated with the project.
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