#!/bin/bash
if pgrep -x "python3" > /dev/null
then
    echo "Бот запущен"
else
    echo "Бот не запущен - перезапуск"
    cd /app
    docx_active=$(ls *.docx)
    echo "Текущий документ:" $docx_active
    nohup python3 bot.py ${docx_active} &
fi