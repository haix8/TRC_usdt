#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
cd $DIR

# if log > 50MB then del log
if [ -e "moni.log" ];then
FILE_SIZE=`du -k "moni.log" | awk '{print $1}'`
if [ $FILE_SIZE -gt 51200 ];then
sudo echo > moni.log
fi;
fi;

PLOG=$DIR/logs/moni.log

PROCESS='tronapi:app'
pid_cs=`ps -ef|grep -v 'grep'|grep -c $PROCESS`

d=$(date "+%Y-%m-%d %H:%M:%S")
echo "*moni->",$d,$pid_cs >>$PLOG
exec 2>>$PLOG

ulimit -c unlimited
source /etc/profile

if [ $pid_cs -eq 0 ]
then
echo "*tronapi->>>pid_cs=0,then restart." >>$PLOG

sh ./start.sh
fi;