#!/bin/bash
echo "Загрузка документа ..." 
input_doc=$(curl -s http://mininform.gov.by/documents/respublikanskiy-spisok-ekstremistskikh-materialov/ | grep -E -io 'href="[^\"]+.doc"' | awk -F\" '{print$2}')
url="http://mininform.gov.by"$input_doc
echo "URL документа:" $url
now=`date +"%Y-%m-%d"`
download=${now}".doc"
docx=${now}".docx"
curl -L $url > $download;

echo "Конвертация документа ..." 
unoconv -d document --format=docx ${download}
rm ${download}

echo "Запуск бота ..." 
python3 bot.py ${docx}