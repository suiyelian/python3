# encoding: utf-8
import re


class CheckSql(object):

    def __init__(self):
        self._pattern = re.compile(r'\(\s*\"\s*call.*?\"', re.S)
        self._endSemicolon = re.compile(r'\(\s*\"\s*call.*?;\s*\"', re.S)
        pass

    def check_sentence(self, path):
        with open(path) as codeFile:
            for line in codeFile:
                for matched in re.findall(self._pattern, line):
                    self.check_sem(matched)

    def check_sem(self, sentence):
        if not re.findall(self._endSemicolon, sentence):
            print("error")
        else:
            print("success")


if __name__ == "__main__":
    test = CheckSql()
    test.check_sentence(r"Regular.txt")



