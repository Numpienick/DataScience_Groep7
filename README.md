# DataScience IMDB Groep 7

## Table of Contents
- [DataScience IMDB-Mover](#datascience-imdb-mover)
  * [Datasets parsing](#datasets-parsing)
  * [Installation](#installation)
    + [Installing Python](#installing-python)
    + [Parsing data](#parsing-data)
  * [Database converter](#database-converter)
    + [Prerequirements](#prerequirements)
    + [Config files](#config-files)
- [DataScience IMDBInfo Web Interface](#datascience-imdbinfo-web-interface)
  * [Features](#features)
  * [Installation](#installation-1)
    + [Installing Django](#installing-django)
    + [Development requirements](#development-requirements)
  * [Running Django Interface](#running-django-interface)
    + [Option A: Starting web interface with PyCharm](#option-a--starting-web-interface-with-pycharm)
    + [Option B: Starting web interface without PyCharm](#option-b--starting-web-interface-without-pycharm)

# DataScience IMDB-Mover
Parser made in Python
>[GitHub Link](https://github.com/Numpienick/DataScience_Groep7)

## Datasets parsing
- Actors
- Actresses
- Cinematographers
- Countries
- Directors
- Movies
- Plot
- Ratings
> The parsing is multithreaded (from raw > CSV. CSV > staging and staging > final)

## Installation
### Installing Python
1. Head to [Python.org](https://www.python.org/downloads/)
2. Download and install Python for the correct platform.
> Because of using certain functions (like match), Python 3.10 is required

### Parsing data
1. Put all .list file datasets in the `data` folder.
2. Open a terminal in the `Parser` folder of the project.
3. Type: `python Controller.py`.
4. You can follow the menu to get your preferred dataset and database.
5. This will take a while, but it will tell you which datasets it has completed.
6. The results (.csv files) will be output in the `output` folder.
4. You can select which datasets you want to be parsed by a number corresponding with the dataset.
5. This will take a while, but it will tell you which datasets it has completed.
6. The results (.csv files) will be output in the `output` folder.

## Database converter
### Prerequirements
* Make sure you have Postgres installed, otherwise head to [Postgresql.org](https://www.postgresql.org/download/) and install it
* Install psycopg2 with `python -m pip install psycopg2` in the terminal.


### Config files
1. First of all you need to add a database.ini in the root of the `Parser` folder
2. Fill it with the correct database settings like this template (default user is postgres):
```
[staging]
host=localhost
database=
user=
password=

[final]
host=localhost
database=
user=
password=
```

# DataScience IMDBInfo Web Interface
Web interface made in Django(Python)

## Features
- Homepage
- Visualisations
- Data of the SQL queries
- Results of different 
- Hypothesis

## Installation
### Installing Django
1. Make sure you have installed Python, if not. Go to the instructions at the Parser instructions.

#### Modules
1. Open terminal and type `python -m pip install Django` and `pip install playsound==1.2.2` (version is important, may have bugs).
2. If you don't have psycopg2 installed, type `python -m pip install psycopg2`.


### Development requirements
1. Make sure Nodejs is installed [Node.js](https://nodejs.org/en/download/)
2. And install sass with `npm i sass -g`
3. Go to settings in PyCharm. (shortcut: ctrl + alt + s)
4. Go to Tools
5. Go to File Watchers
6. Click on the plus icon and add SCSS
7. Scope should be 'project files' and click OK and after that Apply
8. Go to `IMDBInfo/IMDBInfo/settings.py` and change the database settings (current are default settings)


## Running Django Interface
### Option A: Starting web interface with PyCharm
1. Next to the start button, open the dropdown, click edit configurations.
2. Press the plus button and add a Django server.
3. It will tell something about that it doesn't have the right configuration for it, click the FIX button.
4. Here you need to add the root of the Django application, which is the first `IMDBInfo` folder.
5. Also add the settings.py in settings field in the second `IMDBInfo` folder.
6. Go to Settings > Project {Projectname} > Python interpreter.
7. Click the plus button.
8. Add Django, it will install it in your environment now.
9. Now you can start it with the start button in PyCharm.
10. If this doesn't work, go to option B.

### Option B: Starting web interface without PyCharm
1. Open terminal in the first `IMDBInfo` folder.
2. Run the following command: `python manage.py runserver`


