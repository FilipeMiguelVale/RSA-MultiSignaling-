

#
FROM python:3.10

#
WORKDIR /api
#
COPY ./requirements.txt /api/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

#
COPY . .

#COPY ./generate.py ./generate.py
#

CMD ["python3", "generateRSU.py"]
