FROM oliviervg1/centos7
MAINTAINER Olivier Van Goethem <olivier-vg@outlook.com>
ADD requirements.txt /opt/webapp/
ADD ./src /opt/webapp/
WORKDIR /opt/webapp
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
