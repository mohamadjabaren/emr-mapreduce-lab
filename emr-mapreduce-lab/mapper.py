#!/usr/bin/env python
"""mapper.py"""
import sys

def read_input(file):
    for line in file:
        yield line.split()

def main(separator='\t'):
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            cleaned_word = word.rstrip('.,').lower()
            if cleaned_word:
                print('%s%s%d' % (cleaned_word, separator, 1))

if __name__ == "__main__":
    main()
