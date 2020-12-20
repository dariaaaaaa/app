FROM python:3.7

WORKDIR /ds_lab

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/app'

COPY . ./ds_lab

CMD ["python", "./run.py"]
