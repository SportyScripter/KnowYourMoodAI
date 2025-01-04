# Web project setup.

## Create virtual enviorment
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
pip install -r requirements.txt
```

## Run app
```
uvicorn main:app --reload
```