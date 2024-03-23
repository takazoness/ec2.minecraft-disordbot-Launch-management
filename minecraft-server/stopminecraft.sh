#! /bin/bash

# screen name
readonly SCREEN_NAME='minecraft'

if screen -ls | grep -o ${SCREEN_NAME}; then

    # 停止開始
    echo [date '+%F %T'] 'server stop script start'

    # サーバー内にアナウンス
    screen -S $SCREEN_NAME -X stuff 'say 30秒後にサーバーを停止します\n'
    sleep 30s

    # saveコマンド発行
    screen -S $SCREEN_NAME -X stuff 'save-all\n'
    sleep 5s

    # stopコマンド発行
    screen -S $SCREEN_NAME -X stuff 'stop\n'

    # 停止実行待機
    sleep 30s

else
    echo [date '+%F %T'] 'server is not runnning'
fi
