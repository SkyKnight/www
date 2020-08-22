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

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]