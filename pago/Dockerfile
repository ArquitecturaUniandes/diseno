
FROM python:3
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
COPY * /backend/
EXPOSE 5000