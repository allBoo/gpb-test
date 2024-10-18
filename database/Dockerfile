FROM postgres:15

ENV DB_LOG=1

RUN apt-get update && apt-get install -y wget

COPY *.sh /docker-entrypoint-initdb.d/
COPY *.sql /tmp/

RUN chmod a+x /docker-entrypoint-initdb.d/*.sh
RUN chmod a+w /docker-entrypoint-initdb.d/

EXPOSE 5432
