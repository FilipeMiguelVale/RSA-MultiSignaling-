# 
FROM python:3.10

# 
WORKDIR /api

# 
COPY ./requirements.txt /api/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

# 

COPY ./app.py ./app.py
#

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


