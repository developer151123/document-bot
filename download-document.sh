#!/bin/bash

cd /app

echo "Загрузка документа ..."
input_doc=$(curl -s http://mininform.gov.by/documents/respublikanskiy-spisok-ekstremistskikh-materialov/ | grep -E -io 'href="[^\"]+.doc"' | awk -F\" '{print$2}')
doc_file=$(curl -s http://mininform.gov.by/documents/respublikanskiy-spisok-ekstremistskikh-materialov/ | grep -E -io '[a-zA-Z0-9]+.doc')
doc_name=${doc_file%.*}

url="http://mininform.gov.by"$input_doc

echo "URL документа:" $url
echo "Файл:" $doc_file
echo "Документ:" $doc_name

download=${doc_name}".doc"
docx_next=${doc_name}".docx"
docx_current=$(ls *.docx)


download_file() {
  curl -L --max-time 30 $url > $download;
  status="$?"
  echo $status
  zero=0;
  if [[ $status -eq $zero ]];
  then
      echo "Документ загружен"
      echo "Конвертация документа ..." $download
      unoconv -d document --format=docx ${download}
      rm $download
      echo "Документ загружен, новый документ" $docx_next
  else
      rm $download
      echo "Документ  ${docx_next}  не загружен, используем текущий  ${docx_current}"
  fi
}

if [ -e $docx_next ]; then
    echo "Документ уже был загружен ранее " $docx_current
else
    echo 'Необходима загрузка нового документа ' $docx_next
    download_file
fi
