import sys
from typing import Optional
from .template import Processor, Settings
from .datatypes import ANSWER_BOOK_TYPE, ANSWER_DICT_TYPE


class CompareAnswerBook(Processor):

    student_name: str
    student_answer_book: ANSWER_BOOK_TYPE
    standard_answer_book: ANSWER_BOOK_TYPE
    outdir: str

    points: int

    def __init__(self, settings: Settings):
        super().__init__(settings)

    def main(
            self,
            student_name: str,
            student_answer_book: ANSWER_BOOK_TYPE,
            standard_answer_book: ANSWER_BOOK_TYPE):

        self.student_name = student_name
        self.student_answer_book = student_answer_book
        self.standard_answer_book = standard_answer_book

        self.points = 0
        for ipynb in self.standard_answer_book.keys():
            standard_answer_dict = self.standard_answer_book[ipynb]
            student_answer_dict = self.student_answer_book[ipynb]
            self.points += CompareAnswerDict(self.settings).main(
                ipynb=ipynb,
                student_answer_dict=student_answer_dict,
                standard_answer_dict=standard_answer_dict)

        with open(f'{self.outdir}/Summary.txt', 'a', encoding='utf-8') as writer:
            writer.write(f'Total points: {self.points}\n')


class CompareAnswerDict(Processor):

    ipynb: str
    student_answer_dict: ANSWER_DICT_TYPE
    standard_answer_dict: ANSWER_DICT_TYPE

    points: int

    def __init__(self, settings: Settings):
        super().__init__(settings)

    def main(
            self,
            ipynb: str,
            student_answer_dict: ANSWER_DICT_TYPE,
            standard_answer_dict: ANSWER_DICT_TYPE) -> int:

        self.ipynb = ipynb
        self.student_answer_dict = student_answer_dict
        self.standard_answer_dict = standard_answer_dict

        self.points = 0

        for key in self.standard_answer_dict.keys():
            standard_answer = self.standard_answer_dict[key]
            student_answer = self.student_answer_dict.get(key, '')

            is_correct = standard_answer == student_answer

            self.write_to_summary(answer_key=key, is_correct=is_correct)

            if is_correct:
                self.points += get_points(answer_key=key)
            else:
                self.write_correction_file(
                    answer_key=key,
                    standard_answer=standard_answer,
                    student_answer=student_answer)

        return self.points

    def write_to_summary(self, answer_key: str, is_correct: bool):
        x = 'Correct!' if is_correct else 'Wrong'
        with open(f'{self.outdir}/Summary.txt', 'a', encoding='utf-8') as fh:
            fh.write(f'[{self.ipynb}] [{answer_key}] -> {x}\n')

    def write_correction_file(
            self,
            answer_key: str,
            standard_answer: str,
            student_answer: str):
        file = f'{self.outdir}/{self.ipynb} {answer_key}.txt'
        text = f'''\
---CORRECT ANSWER---
{standard_answer}
---STUDENT ANSWER---
{student_answer}'''
        with open(file, mode='w', encoding='utf-8') as fh:
            fh.write(text)


def get_points(answer_key: str) -> Optional[float]:
    """
    '# ANSWER (1.5 point)' -> 1.5
    '# ANSWER (1.5 points)' -> 1.5
    """

    try:
        points = float(answer_key.split(' (')[1].split(' point')[0])
    except Exception as e:
        points = None
        print(e, file=sys.stderr)
    return points
