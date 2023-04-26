docker-compose up --scale python-worker=2 --build
pip install -r requirements.txt --index-url=https://pypi.python.org/simple