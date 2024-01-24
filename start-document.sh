#!/bin/bash

# Останавливаем бот
pkill -f python3
cd /app

./download-document.sh

#Удалить все документы кроме последнего
echo "Перед чисткой:"
ls -l *.docx
ls -t *.docx| tail -n+2 | xargs rm --
echo "После чистки:"
ls -l *.docx

docx_active=$(ls *.docx)
echo "Текущий документ:" $docx_active

#Запускам бот с самым последним файлом
python3 bot.py ${docx_active}
