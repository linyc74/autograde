from setuptools import setup, find_packages


def get_version() -> str:
    with open('autograde/__init__.py') as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]


def main():
    setup(
        name='autograde',
        version=get_version(),
        description='Automatic grading for Jupyter Notebook',
        url='https://github.com/linyc74/autograde',
        author='Yu-Cheng Lin',
        author_email='ylin@nycu.edu.tw',
        license='MIT',
        packages=find_packages(),
        python_requires='>3.6',
        install_requires=[],
        zip_safe=False
    )


if __name__ == '__main__':
    main()
    # python setup.py sdist
