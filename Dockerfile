# Based on instructions at https://fastapi.tiangolo.com/deployment/docker/

# 
FROM python:3.8.17

# 
WORKDIR /code/app

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
