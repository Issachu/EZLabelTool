From ubuntu:18.04
MAINTAINER PingyiHu
COPY . /app
WORKDIR /app
#安装所需依赖
RUN apt-get update \
&& apt-get install -y nodejs npm \
&& npm install
EXPOSE 3000
CMD ["npm", "start", "run"]
ENV LC_ALL=C.UTF-8
ENV LANF=C.UTF-8
