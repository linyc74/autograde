import os
import json
from io import StringIO
from typing import Dict, List
from contextlib import redirect_stdout
from .tools import get_files
from .datatypes import ANSWER_BOOK_TYPE, ANSWER_DICT_TYPE
from .code_text import TextLinesToCode, ModifyCodeToReprTheLastLine


class RunEntireFolderToAnswerBook:

    folder: str

    ipynbs: List[str]
    answer_book: ANSWER_BOOK_TYPE

    def main(self, folder: str) -> ANSWER_BOOK_TYPE:
        self.folder = os.path.abspath(folder)

        self.set_ipynbs()
        self.answer_book = {}

        for ipynb in self.ipynbs:
            answer_dict = RunNotebookToAnswerDict().main(ipynb=ipynb)
            self.answer_book[os.path.basename(ipynb)] = answer_dict

        return self.answer_book

    def set_ipynbs(self):
        self.ipynbs = get_files(
            source=self.folder,
            endswith='.ipynb',
            isfullpath=True)


class RunNotebookToAnswerDict:

    ipynb: str

    original_context_dir: str
    ipynb_context_dir: str

    cells: List[Dict]
    answer_dict: ANSWER_DICT_TYPE

    def __init__(self):
        self.modify_last_line = ModifyCodeToReprTheLastLine().main

    def main(self, ipynb: str) -> ANSWER_DICT_TYPE:
        self.ipynb = os.path.abspath(ipynb)

        self.set_cells()
        self.set_context_dirs()
        self.answer_dict = {}

        os.chdir(self.ipynb_context_dir)
        for cell in self.cells:

            if cell['cell_type'] != 'code':
                continue

            code = TextLinesToCode().main(text_lines=cell['source'])

            if code.startswith('# ANSWER '):
                code = self.modify_last_line(code)

            try:
                with redirect_stdout(StringIO()) as f:
                    exec(code)
                result = f.getvalue()
            except Exception as e:
                result = f'{type(e)}: {e}'

            if code.startswith('# ANSWER '):
                answer_id = code.splitlines()[0]
                self.answer_dict[answer_id] = result

        os.chdir(self.original_context_dir)

        return self.answer_dict

    def set_original_context_dir(self):
        self.original_context_dir = os.path.abspath(os.curdir)

    def set_cells(self):
        with open(self.ipynb, encoding='utf-8') as fh:
            notebook_str = json.loads(fh.read())
        self.cells = notebook_str['cells']

    def set_context_dirs(self):
        self.original_context_dir = os.path.abspath(os.curdir)
        self.ipynb_context_dir = os.path.dirname(self.ipynb)
