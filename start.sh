#!/bin/bash

TIMESTAMP=$(date +%s)
SOCKET="/tmp/tldrizer/tldrizersocket"$TIMESTAMP
mkdir /tmp/tldrizer
THIS_PID=$$
# PROGRAM="/path/to/my/program"

# echo $TIMESTAMP
# docker compose run --rm tldrizer bash -c "python /tldrizer/main.py --sockets_timestamp $TIMESTAMP"
docker compose run --rm -d tldrizer bash -c "python /tldrizer/main.py --sockets_timestamp $TIMESTAMP"

# ech ollega
while true; do
  nc -lU "$SOCKET" | while read -r MESSAGE; do
    # echo "start" | nc -q 0 -U "/tmp/mysocket"
    # echo "do" | nc -q 0 -U "/tmp/mysocket"

    # if [[ "$MESSAGE" == "start" ]]; then
    #   echo "start"
    # elif [[ "$MESSAGE" == "do" ]]; then
    #   echo "do"
    # fi
    
    
    # mpv --input-ipc-server=/tmp/mpvsocket 
    # echo '{ "command": ["seek", "00:00:30", "absolute"] }' | socat - /tmp/mpvsocket


    # echo "mpv https://youtu.be/aGi17bA_dXU" | nc -q 0 -U "/tmp/mysocket"
    # echo "mpv https://youtu.be/aGi17bA_dXU --input-ipc-server=/tmp/mpvsocket" | nc -q 0 -U "/tmp/mysocket"
    # echo '{ "command": ["seek", "00:00:30", "absolute"] }' | socat - /tmp/mpvsocket
    # echo "kill \$THIS_PID" | nc -q 0 -U "/tmp/mysocket"
    eval "$MESSAGE"

  done
done
