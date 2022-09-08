import os
import pandas as pd
from .compare import CompareAnswerBook
from .datatypes import ANSWER_BOOK_TYPE
from .template import Settings, Processor
from .answer_book import RunEntireFolderToAnswerBook


class Autograde(Processor):

    standard_dir: str
    student_dir: str

    standard_answer_book: ANSWER_BOOK_TYPE
    student_answer_book: ANSWER_BOOK_TYPE

    def __init__(self, settings: Settings):
        super().__init__(settings)

    def main(self, standard_dir: str, student_dir: str):
        self.standard_dir = standard_dir
        self.student_dir = student_dir

        self.pandas_global_config()
        self.set_standard_answer_book()
        self.set_student_answer_book()
        self.compare_answer_book()

    def pandas_global_config(self):
        # Global settings to capture complete dataframe in stdout
        pd.set_option('expand_frame_repr', None)
        pd.set_option('display.max_rows', None)

    def set_standard_answer_book(self):
        self.standard_answer_book = RunEntireFolderToAnswerBook().main(
            folder=self.standard_dir)

    def set_student_answer_book(self):
        self.student_answer_book = RunEntireFolderToAnswerBook().main(
            folder=self.student_dir)

    def compare_answer_book(self):
        CompareAnswerBook(self.settings).main(
            student_name=os.path.basename(self.student_dir),
            standard_answer_book=self.standard_answer_book,
            student_answer_book=self.student_answer_book)
