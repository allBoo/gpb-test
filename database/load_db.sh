#!/bin/bash

get_url(){
    URI=$1;
    LOCAL_FILE=$2;
    FILE_NAME=$3;

    if [ "$URI" == "" ]
    then
        echo "A URL to a $FILE_NAME must be specified."
        exit 1;
    fi

    proto="$(echo $URI | grep :// | sed -e's,^\(.*://\).*,\1,g')"
    url="$(echo ${URI/$proto/})"
    if [ "$proto" == "" -o "$url" == "" ]
    then
        echo "$FILE_NAME URL must be in the format protocol://path/to/ini [$proto$url]."
        exit 1;
    fi

    proto="$(echo ${proto} | tr '[:upper:]' '[:lower:]')"
    if [ "$proto" == "file://" ]
    then
        echo "Pulling local file from $url";
        cp $url $LOCAL_FILE;
    elif [ "$proto" == "s3://" ]
    then
        echo "Pulling s3 file from $url";
        aws s3 cp $URI $LOCAL_FILE;
    else
        echo "Pulling remote file from $URI";
        wget $URI -O $LOCAL_FILE;
    fi
}

if [ -z $POSTGRES_USER ]
then
  echo "POSTGRES_USER env must be set"
  exit
fi

if [ -z $POSTGRES_DB ]
then
  echo "POSTGRES_DB env must be set"
  exit
fi

if [ "$DB_URL" == "" ]
then
	echo "DB_URL env must be set"
    exit
fi

if [ "$DB_LOG" == "on" ]
then
	echo "DB_LOG is set, turning on logging.";
	perl -pi -e "s/#log_statement = 'none'/log_statement = 'all'/g" /var/lib/postgresql/data/postgresql.conf;
	perl -pi -e "s/#log_duration = off/log_duration = on/g" /var/lib/postgresql/data/postgresql.conf;
else
	echo "DB_LOG [$DB_LOG]is not set, no logging.";
fi

if [ ${DB_URL: -3} == ".gz" ]
then
  get_url "$DB_URL" "/docker-entrypoint-initdb.d/99_latest_anon.sql.gz" "GZipped dump file"

	echo "Uncompressing DB";
	gunzip /docker-entrypoint-initdb.d/99_latest_anon.sql.gz;
else
  get_url "$DB_URL" "/docker-entrypoint-initdb.d/99_latest_anon.sql" "Dump file"
fi

psql -U "$POSTGRES_USER" "$POSTGRES_DB" < /docker-entrypoint-initdb.d/99_latest_anon.sql;
rm /docker-entrypoint-initdb.d/99_latest_anon.sql;
