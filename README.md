# project_new_space 
## The Server of StarTracker app
project_new_space is a server application built with FastAPI.<br /> It takes an image path of stars, performs the algorithm on the image, and returns a list of star IDs, names, and coordinates.

<img width="200" src="photo/צילום מסך 2023-06-05 133258.png">

## Algorithm:


## Installation
1. clone this repository
2. Install the dependencies: pip install -r requirements.txt
3.  run the following command in the terminal to start the server:<br />
```uvicorn server:app --host <server network address> --port 8080 --reload``` <br />
**Note.** Verify that the phone and the server are connected to the same network (Wi-Fi, Ethernet, eg.)
