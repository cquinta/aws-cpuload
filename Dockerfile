FROM python
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN apt-get update -y
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python3 app.py