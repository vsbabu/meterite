#!/bin/bash
METRICS=("M1" "M2" "M3" "M4" "M5")
for m in "${METRICS[@]}"
do
  curl -X POST "http://127.0.0.1:8000/metric/" \
       -H  "accept: application/json" \
       -H  "Content-Type: application/json" \
       -H "X-Auth-Token: 123456" \
       -d "{\"code\":\"$m\",\"name\":\"$m name\",\"active\":true,\"min_reading\":-99999,\"max_reading\":99999, \"truncate_reading_to\": \"minute\"}"
done
#for 1000 minutes down to 10 at steps of 10,
#pick a random metric and add a random value
for s in `seq 100 -10 10`; do
  d=`date -Iseconds -d "- $s minutes"`
  v=$(( $RANDOM % 100 ))
  m=${METRICS[$RANDOM % ${#METRICS[@]}]}
  curl -X POST "http://127.0.0.1:8000/metric/$m" \
       -H  "accept: application/json" \
       -H  "Content-Type: application/json" \
       -H "X-Auth-Token: 123456" \
       -d "{\"reading\":$v,\"reading_at\":\"$d\"}" &
done
