# Honeycomb Compass - Model and Rest API
## _by Martin Lorenzo_

This is a project related to the Web UI of a code challenge called Honeycomb Compass, which stands:

> Honeycomb Compass
 >
> A bee researcher discovered how to improve honey production by guiding bees in a honeycomb to certain cells, in such a way that arranging a group of bees in a very specific layout, their production as a team is greatly improved.
>
> The honeycomb is an N by N rectangular shape. The location of a bee in the honeycomb is identified by x and y coordinates of the cell, and the orientation (that is, the cardinal point where the bee is pointing at: North, South, East and West). Bees move from one cell to the other one in single step movements and can rotate left/right within a cell.
> 
> The initial position for such a design is 0,0,N, which identifies a bee located in the bottom left corner and facing North. The cell directly to the North from x, y is x,y+1.
 
> In order to guide a bee to its final location, the researcher designed a bio-interface to trigger the following actions:
 
> Spin 90 degrees left or right, without moving from its current spot: in this case, the bio-interface accepts commands L and R, for left and right rotation respectively
Move forward one cell in the honeycomb, maintain the same heading: in this case, the bio-interface accepts command M
 
> Model and algorithmic
Design and implement a system to support the researcher's bio-interface. The system expects:
One line for the honeycomb's upper-right coordinates (lower-left coordinates are assumed to be 0,0), which is used to initialize the honeycomb.
> Two lines per bee:
1st line indicates the initial position and heading where the bee is initially placed
2nd line indicates a stream of instructions to guide the bee
The output for each stream processed is the final position and heading where the bee ended up.

> Example
Input
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
Expected Output
1 3 N
5 1 E
 
> ---------
> Rest API
Since the bio-interface device is meant to be used by different researchers to conduct experiments, you are asked to design and implement a robust REST API using Flask that allows to operate remotely, re-using the system defined above.

> Web UI
Create a Web UI using React (latest versions) to visualize:
Honeycomb grid: the user enters the shape of the honeycomb so it can be initialized and rendered
Bee tour: the user specifies where the bee starts, where is heading to, and visualizes it in the honeycomb
Final position: the user enters instructions for a specific bee, and visualizes the final position

## Considerations taken from the honeycomb compass statement

- More than one bee can stay in the same cell
- A move in the honeycomb is considered as a move for all the bees in it, at the same time. Even if a bee has covered all steps in it's sequence, will be considered as a 'no move' move
- If the sequence of moves makes the bee go outside (or fall) from the honeycomb, is considered as 'Dissapeared'. This means once a bee is out, it can't come back.
- The user can decide to simulate one step at a time, or jump into the latest move
- The user can reset the honeycomb to the initial position


## Feature

- A model that meet the requierements of the bee researcher and the considerations mentioned above
- Unit testing ensuring also the business logic of the model (messages on assertions are WIP). API testing is pending, only some json schemas checks were made
- Error hadling using Exceptions and default response data
- A Rest API so that it can be consumed as a service from several clients

## Tech

Libraries and tools used for this development:

- [Flask] - A web framework that lets us develop web applications easily
- [Pytest] - The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries
- [PyCharm] - PyCharm is a hybrid platform developed by JetBrains as an IDE for Python.
- [Jsonschema] - jsonschema is an implementation of the JSON Schema specification for Python.
- [Postman] - Postman is an API platform for building and using APIs.

## Installation

Honeycomb Compass - Model and Rest API requires [pip] in order to be installed and run
First is important to set up the virtual environment ([venv])
Then install the dependencies with the command
```sh
pip install -r requirements.txt
```
To run the model and test on the console, navigate to the model/honeycomb folder and run the honeycomb.py file
```sh
cd src/model/src/honeycomb
python3 honeycomb.py
```
To run the API, just run the wsgi.py file from the root of the project
 ```sh
python3 wsgi.py
```
The Rest API should start running on port 5000

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - )

   [pip]: <https://pypi.org/project/pip/>
   [Flask]: <https://flask.palletsprojects.com/en/2.1.x/>
   [Jsonschema]: <https://python-jsonschema.readthedocs.io/en/stable/>
   [Pytest]: <https://docs.pytest.org/en/7.1.x/>
   [PyCharm]: <https://www.jetbrains.com/es-es/pycharm/>
   [Postman]: <https://www.postman.com/>
   [venv]: <https://docs.python.org/3/library/venv.html>
