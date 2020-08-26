FROM python:2.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# https://github.com/DefectDojo/django-DefectDojo/issues/407#issuecomment-415862064
RUN sed '/st_mysql_options options;/a unsigned int reconnect;' /usr/include/mysql/mysql.h -i.bkp
WORKDIR /usr/src/app
COPY req_parafia.txt ./
RUN pip install -r req_parafia.txt
COPY . .

# https://www.datanovia.com/en/lessons/docker-compose-wait-for-container-using-wait-tool/docker-compose-wait-for-mysql-container-to-be-ready/
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

EXPOSE 80
#CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
CMD sh -c "/wait && python manage.py runserver 0.0.0.0:80"