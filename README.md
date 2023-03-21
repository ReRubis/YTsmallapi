# API for... YouTube API?  
Form request to request something from YouTube

# Installation
Preferable method is to use devcontainer
1. install the `Remote-Containers` VS-code extenstion
2. open the project folder
3. rebuild and open the folder in container.

# Running
1. Make sure that the virtual environment is opened. 

```sh
. ./.venv/bin/activate
```
3. Run the uvicorn
```sh
uvicorn yutservice.main:app --reload
```
No front-end, but it's possible to use interactive swagger documentation,
by adding /docs at the end of localhost:8000 . 