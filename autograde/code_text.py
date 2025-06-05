from typing import List


class TextLinesToCode:

    text_lines: List[str]
    code: str

    def main(self, text_lines: List[str]) -> str:
        self.code = ''
        for line in text_lines:
            self.code += line.rstrip() + '\n'
        self.code = self.code.replace('%matplotlib inline', '')
        self.code = self.code.replace('plt.show()', '')
        return self.code


class ModifyCodeToPrintTheLastLine:

    lines: List[str]

    def main(self, code: str) -> str:
        self.lines = code.splitlines()

        last_line = self.lines[-1]
        if not last_line.startswith('print'):
            self.lines[-1] = f'print({last_line})'

        return '\n'.join(self.lines)
