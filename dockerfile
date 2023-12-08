FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000


CMD ["uvicorn", "d2site.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
