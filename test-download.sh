#!/bin/bash
echo "Загрузка документа ..." 
input_doc=$(curl -s http://mininform.gov.by/documents/respublikanskiy-spisok-ekstremistskikh-materialov/ | grep -E -io 'href="[^\"]+.doc"' | awk -F\" '{print$2}')
url="http://mininform.gov.by"$input_doc
echo "URL документа:" $url
now=`date +"%Y-%m-%d"`
download=${now}".doc"
docx=${now}".docx"
(curl -L --max-time 30 $url > $download;) | /bin/bash -s >/dev/null 2>&1
rc=$?
if [ -z "$rc" ]
then
    echo "Документ загружен"

    echo "Конвертация документа ..." $download
else
    rm $download
    docx=$(ls *.docx)
    echo "Документ не загружен, используем текущий " $docx 
fi  
