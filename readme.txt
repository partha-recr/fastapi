mkdir fastapi_app
cd fastapi_app
python -m venv venv  # Create virtual environment
venv\Scripts\activate
pip install fastapi uvicorn
uvicorn main:app --reload
pip freeze > requirements.txt
#!/bin/bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

