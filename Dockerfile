FROM ubuntu:22.04
COPY ./ /app
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip build-essential
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
