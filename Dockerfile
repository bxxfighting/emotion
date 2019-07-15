FROM python:3.6.8
MAINTAINER bxx 305526954@qq.com

ADD ./sources.list /etc/apt/
RUN apt-get update
RUN apt-get -y --force-yes install vim

RUN mkdir /project
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN chmod 755 /project/start.sh
EXPOSE 12321
CMD ["/project/start.sh"]
