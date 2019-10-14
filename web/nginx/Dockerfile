FROM nginx


#对外暴露端口
EXPOSE 80 8000

RUN rm /etc/nginx/conf.d/default.conf

ADD nginx.conf  /etc/nginx/conf.d/
RUN mkdir -p /opt/nginx/static
RUN mkdir -p /opt/nginx/html
RUN mkdir -p /opt/nginx/excel
