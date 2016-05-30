# using alpine because it's the smallest i can use
FROM alpine:3.3

# whoami
MAINTAINER naor livne <naorlivne@gmail.com>

#install python and pip
RUN apk add --update python py-pip

#add the codebase
RUN mkdir /dshp
COPY ./ ./dshp/
RUN chmod +x /dshp/dshp.py

#set python to be unbuffered
ENV PYTHONUNBUFFERED=1

#expose defult port - you will need to change it if you config it to another one
EXPOSE 8888

#run DSHP
WORKDIR /dshp
CMD python /dshp/dshp.py