# Web project setup.
## Create virtual enviorment
Set on root project ./KnowYourMoodAI and make commands from there.
To create a virtual environment, use the `venv` module that comes with Python.
```
python -m venv .venv
```

## Activate virtual enviorment
To activate new virtual enviorment, use following command
```
source .venv/bin/activate
```

## Upgrade pip
```
python -m pip install --upgrade pip
```

## Install packages
```
pip install -r WebApp/requirements.txt
```

## Run app
```
uvicorn WebApp.main:app --reload
```
## Run local server for Android device access (same network)
```
uvicorn WebApp.main:app --host 0.0.0.0 --port 8000
```

## After starting the server, find your device's IPv4 address enter in cmd "ipconfig" and use it on Android: 

```
Example: 192.168.1.100:8000
```