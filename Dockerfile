FROM pardus/yirmibir
COPY ./ /app
COPY ./web/default.conf /etc/nginx/conf.d
COPY ./web/fastcgi_params /etc/nginx/fastcgi_params
COPY ./web/fastcgi.conf /etc/nginx/fastcgi.conf
WORKDIR /app
RUN apt-get update && apt-get install python3 python3-pip 
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
