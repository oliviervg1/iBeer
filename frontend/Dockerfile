FROM oliviervg1/centos7
MAINTAINER Olivier Van Goethem <olivier-vg@outlook.com>
ADD ./src /opt/webapp/
ADD package.json /opt/webapp/
WORKDIR /opt/webapp
RUN npm install
EXPOSE 5001
CMD ["npm", "start"]
