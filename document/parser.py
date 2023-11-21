import logging
from typing import NamedTuple
from docx import Document
from difflib import SequenceMatcher

#
class DocumentRow(NamedTuple):
    type: list
    text: list
    justification: list

DocumentRows = []

logger = logging.getLogger(__name__)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def load_document(filename):
    logger.log(level=logging.INFO, msg="Начало загрузки документа")

    DocumentRows.clear()
    document = Document(filename)
    rows = 0
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
            print("Загружено строк ", rows)

    logger.log(level=logging.INFO, msg="Конец загрузки документа, прочитано  " + str(rows) + " строк")


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