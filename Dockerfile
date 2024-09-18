FROM python:3.10

RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN mkdir /app

COPY requirements.txt /app/

RUN python -m pip install -r /app/requirements.txt

COPY wallet_project/ /app/wallet_project/

EXPOSE 8000

WORKDIR /app/wallet_project

CMD ["python", "manage.py", "migrate"]