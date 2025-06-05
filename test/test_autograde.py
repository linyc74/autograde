from autograde.autograde import Autograde
from .setup import TestCase


class TestAutograde(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_bad_grade(self):
        Autograde(self.settings).main(
            standard_dir=f'{self.indir}/homework_standard',
            student_dir=f'{self.indir}/homework_bad_grade_student'
        )

        self.assertFileEqual(
            f'{self.indir}/Summary-bad-grade.txt',
            f'{self.outdir}/Summary.txt',
        )

    def test_good_grade(self):
        Autograde(self.settings).main(
            standard_dir=f'{self.indir}/homework_standard',
            student_dir=f'{self.indir}/homework_good_grade_student'
        )

        self.assertFileEqual(
            f'{self.indir}/Summary-good-grade.txt',
            f'{self.outdir}/Summary.txt',
        )

    def test_missing_ipynb(self):
        Autograde(self.settings).main(
            standard_dir=f'{self.indir}/homework_standard',
            student_dir=f'{self.indir}/homework_missing_ipynb_student'
        )
        self.maxDiff = None
        self.assertFileEqual(
            f'{self.indir}/Summary-missing-ipynb.txt',
            f'{self.outdir}/Summary.txt',
        )

    def test_plt_show(self):
        """
        Test that plt.show(), if any, should be removed prior to execution,
        because plt.show() halts execution in a non-interactive environment.
        plt.show() also does return anything, so should not affect student's grade.
        """
        Autograde(self.settings).main(
            standard_dir=f'{self.indir}/homework_standard',
            student_dir=f'{self.indir}/homework_plt_show_student'
        )
