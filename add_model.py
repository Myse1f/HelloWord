#!/usr/bin/env python3
# coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HelloWord.settings")


import django
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from words.models import Vocabulary
from words.models import Word

CET4 = Vocabulary.objects.create(name='四级')
CET6 = Vocabulary.objects.create(name='六级')
POST = Vocabulary.objects.create(name='考研')
IELTS = Vocabulary.objects.create(name='雅思')
TOEFL = Vocabulary.objects.create(name='托福')
data = {
    'IELTS.txt': IELTS,
    'TOEFL.txt': TOEFL,
    'CET4.txt': CET4,
    'CET6.txt': CET6,
    'POST.txt': POST

}


def create(filename, vocabulary):
    with open(filename) as f:
        for line in f:
            name, explanation =\
                line.split('|')[0], line.split('|')[1].strip('\n')
            example = 'This an example for {}'.format(name) # pretend it's an example
            word = Word.objects.create(name=name, explanation=explanation, example=example)
            vocabulary.words.add(word)
    print('{}导入完成'.format(filename))


def main():
    for x, y in data.items():
        create(x, y)


if __name__ == "__main__":
    main()
    print('Done!')
