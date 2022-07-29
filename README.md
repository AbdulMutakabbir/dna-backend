# dna-backend

## deployment

* git clone https://github.com/AbdulMutakabbir/dna-backend.git
* cd dna-backend/
* python3 -m venv ./venv
* source ./venv/bin/activate
* pip3 install -r requirements.txt
* pip3 install gunicorn
* nohup gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &
