#!/bin/bash

crontab -u root -r

# Останавливаем бот
pkill -9 -f python3
cd /app

./download-document.sh

#Удалить все документы кроме последнего
echo "Перед чисткой:"
ls -l *.docx
ls -t *.docx| tail -n+2 | xargs rm --
echo "После чистки:"
ls -l *.docx

if pgrep -x "python3" > /dev/null
then
    pkill -9 -f python3
fi

#Запускаем бот с самым последним файлом
docx_active=$(ls *.docx)
echo "Текущий документ:" $docx_active
nohup python3 bot.py ${docx_active} &
echo "Бот стартовал"

(crontab -u root -l ; echo "*/15 * * * * bash /app/download-document.sh >> /var/log/cron.log 2>&1" ) | crontab -u root -
(crontab -u root -l ; echo "*/5 * * * * bash /app/restart-document.sh >> /var/log/cron.log 2>&1" ) | crontab -u root -
(crontab -u root -l ; echo "0 1 * * * bash /app/start-document.sh >> /var/log/cron.log 2>&1" ) | crontab -u root -
echo "Выход из скрипта"