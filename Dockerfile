FROM python:3.7

WORKDIR /ds_lab

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/ds_lab'

COPY . ./ds_lab

CMD ["python", "./run.py"]
