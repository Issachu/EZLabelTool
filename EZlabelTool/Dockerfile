From python:3.8
MAINTAINER PingyiHu
COPY . /app
WORKDIR /app
#install the requirements
RUN cd back-end \
&& pip install -r requirements.txt
EXPOSE 5000
WORKDIR /app/back-end
CMD ["flask", "run", "--host=0.0.0.0"]
ENV LC_ALL=C.UTF-8
ENV LANF=C.UTF-8