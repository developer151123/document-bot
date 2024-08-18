import errno
import logging
import os
import re
from typing import NamedTuple

import xlsxwriter
from docx import Document
from difflib import SequenceMatcher

#
class DocumentRow(NamedTuple):
    type: list
    text: list
    justification: list

class DocumentLink(NamedTuple):
    link: str
    justification: list


DocumentRows = []
DocumentLinks = []


logger = logging.getLogger(__name__)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def load_document(filename):
    logger.log(level=logging.INFO, msg="Начало загрузки документа")

    DocumentRows.clear()
    DocumentLinks.clear()

    document = Document(filename)
    rows = 0
    regex_pattern = re.compile(r't\.me/[a-zA-Z0-9_.-]+')

    for table in document.tables:
        for row in table.rows:
            rows += 1
            row_cells = []
            for cell in row.cells:
                cell_para = []
                for para in cell.paragraphs:
                    cell_para.append(para.text)
                row_cells.append(cell_para)
            DocumentRows.append(DocumentRow(type=row_cells[0],text=row_cells[1],justification=row_cells[2]))

            link_found = False
            for cell_para in row_cells[1]:
                for match in regex_pattern.finditer(cell_para):
                    DocumentLinks.append(DocumentLink(link=match.group(),justification=row_cells[2]))

            print("Загружено строк ", rows)
            print("Найдено линков ", len(DocumentLinks))

    logger.log(level=logging.INFO, msg="Конец загрузки документа, прочитано  " + str(rows) + " строк")
    print("Запись линков в файл ")
    write_links()

def is_not_blank(s):
    return bool(s and not s.isspace())

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def write_links():

    silentremove('telegram-links.xlsx')
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('telegram-links.xlsx')
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 200)

    # Write some simple text.
    worksheet.write('A1', 'Ссылки на каналы')
    worksheet.write('B1', 'Решения суда')

    row = 1
    for link in DocumentLinks:
        worksheet.write(row, 0, link.link)
        text = ''
        for para in link.justification:
            if is_not_blank(para):
                text += para + '\n'

        if is_not_blank(text):
            worksheet.write(row, 1, text)
        row += 1

    workbook.close()


def parse_document(text):
    foundRows = []
    logger.log(level=logging.INFO, msg="Начало поиска последовательности " + text )
    for row in DocumentRows:
        for para in row.text:
            if text.casefold() in para.casefold():
                foundRows.append(row)
                break

    logger.log(level=logging.INFO, msg="Конец поиска последовательности " + text)
    return foundRows


def get_row(n):
    return DocumentRows[n]