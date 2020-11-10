#!/bin/bash

# 用于寻找进程的关键字

PROCESS=tronapi:app

# 通过"tronapi:app"找到并杀掉之前的进程
for pid in $(ps aux | grep -v 'grep' | grep $PROCESS | awk '{print $2}')
do
  if [ "$pid" != "" ]
  then
#    echo "killing $pid"
    kill -9 $pid
  fi
done
