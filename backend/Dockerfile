FROM python:3
WORKDIR /opt/ibeer
COPY requirements.txt ./
COPY ./src ./
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
