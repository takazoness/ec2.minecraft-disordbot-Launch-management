#! /bin/bash

# screenの名前
readonly SCREEN_NAME='minecraft'

screen -AmdS $SCREEN_NAME java -Xmx1024M -Xms1024M -Dlog4j2.formatMsgNoLookups=true -jar server.jar nogui pause
