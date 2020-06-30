README P5:

# HealthySubstitute

This application finds a food substitute for a given product, based on parsed then saved data from the Open food facts Api.
User experience is guided through a series of question grouped by menus, in order to find a healthy substitute in accordance with user choices. For convenience of use, the healthy substitute could be saved in a favourite list.

## Data base preparation

User should have already created his data base to recieve Open food facts data. Once the data base is created, user need to enter personal necessary pieces of information related to the user and his data base. This must be done by modifying the file named dbuser.py where user have to modify each value into the key, value pairs structure named config.
User should then execute the module dbbuilder in order to have data stored in tables and ready to be used.


## Installation

1. Clone this code with `git clone https://github.com/BENBELGACEM-Bassem/P5.git`
2. Use the file requirements.txt to install needed pacakges with pip install -r requirements.txt
3. Go to the project with `cd P5/healthy_substitute`


## Start

Once the virtual environment acivated:

- fill user database with parsed data from Open food facts Api with:
`python load.py`

- start the application, in the terminal with:
`python main.py`


