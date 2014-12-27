FROM centos:centos7
MAINTAINER Olivier Van Goethem <olivier-vg@outlook.com>
RUN yum update -y && yum install epel-release -y 
RUN yum install npm python-pip -y
