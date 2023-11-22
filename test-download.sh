#!/bin/bash
echo "Загрузка документа ..." 
input_doc=$(curl -s http://mininform.gov.by/documents/respublikanskiy-spisok-ekstremistskikh-materialov/ | grep -E -io 'href="[^\"]+.doc"' | awk -F\" '{print$2}')
url="http://mininform.gov.by"$input_doc
echo "URL документа:" $url
url1="http://mininform2.gov.by"$input_doc

now=`date +"%Y-%m-%d"`
download=${now}".doc"
docx=${now}".docx"
curl -L --max-time 30 $url > $download;
status="$?"
echo $status
zero=0;
if [[ $status -eq $zero ]];
then
    echo "Документ загружен"
    echo "Конвертация документа ..." $download
else
    rm $download
    docx=$(ls *.docx)
    echo "Документ не загружен, используем текущий " $docx 
fi  
