# DataScience IMDB Groep 7

##Table of content
- DataScience IMDB-Parser
- DataScience IMDBInfo

# DataScience IMDB-Parser
Parser made in Python

## Datasets parsing
- Actors
- Actresses
- Cinematographers
- Countries
- Directors
- Movies
- Plot
- Ratings

## Installation
### Installing Python
1. Head to [Python.org](https://www.python.org/downloads/)
2. Download and install Python for the correct platform.
#### Because of using certain functions, Python 3.10 is required

### Parsing data
1. Put all .list file datasets in the `data` folder.
2. Open a terminal in the `Parser` folder of the project.
3. Type: `python Parser.py`.
4. You can select which datasets you want to be parsed by a number corresponding with the dataset.
5. This will take a while, but it will tell you which datasets it has completed.
6. The results (.csv files) will be output in the `output` folder.
4. You can select which datasets you want to be parsed by a number corresponding with the dataset.
5. This will take a while, but it will tell you which datasets it has completed.
6. The results (.csv files) will be output in the `output` folder.



# DataScience IMDBInfo
Web interface made in Django(Python)

## Features
- Search
- 

## Installation
### Installing Django
1. Make sure you have installed Python, if not. Go to the instructions at the Parser
2. Open terminal and type `python -m pip install Django`
3. If you don't have psycopg2 installed, type `python -m pip install psycopg2`

### Starting web interface with PyCharm
1. Next to the start button, open the dropdown, click edit configurations.
2. Press the plus button and add a Django server.
3. It will tell something about that it doesn't have the right configuration for it, click the FIX button.
4. Here you need to add the root of the Django application, which is the first `IMDBInfo` folder.
5. Also add the settings.py in settings field in the second `IMDBInfo` folder.
6. Go to Settings > Project {Projectname} > Python interpreter.
7. Click the plus button.
8. Add Django, it will install it in your environment now.
9. Now you can start it with the start button in PyCharm.

### Starting web interface without PyCharm
1. Open terminal in the first `IMDBInfo` folder.
2. Run the following command: `python manage.py runserver`

