# notreaddit

notreaddit is an Information Retrieval (IR) system that creates semantic graphs for each document for better visualization.

## Requirements

- Ubuntu 18.04 (Works with other OS as well, might need to modify few commands)
- Python 3 (Tested with Python 3.7)

   ```bash
      sudo apt install python3
- [pip](https://pip.pypa.io/en/stable/)

   ```bash
      sudo apt install python3-pip
   ```


## Installation

- Use the package manager pip to install virtualenv. You can skip this step to install in your workspace, but virtualenv is highly recommended.

    ```bash
    pip3 install virtualenv
    ```
- Either clone the repository from git or copy the contents of the attached zip folder to the current folder.
    ```bash
    git clone https://kgcoe-git.rit.edu/ns9805/notreaddit.git
    ```
- Create a virtual environment and activate it.
    ```bash
    python3 -m virtualenv venv
    source venv/bin/activate
- Install all the required dependencies.
    ````bash
    pip3 install -r requirements.txt
- Run the `setup.py` file to setup other libraries.
    ````bash
    python3 setup.py
## Usage

```bash
python3 notreaddit.py
```

## Output
The python script reads all the JSON objects in the `data.json` file and creates a VSM. 

When a query is passed, it performs a ranked retrieval using cosine proximity and returns a list of documents (articles), ordered from most to least relevant.

For each document, a basic structure of the aforementioned semantic graph/tree is also displayed. If you do no have the appropriate libraries installed, or if the code is deployed on a headless server instance, the tree is printed onto the terminal.