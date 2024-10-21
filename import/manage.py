#!/usr/bin/env python
import os
import sys

def main():
    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, 'src')

    sys.path.insert(1, path)

    from src.cli import run
    run()


if __name__ == '__main__':
    main()
