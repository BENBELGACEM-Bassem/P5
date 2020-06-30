#! P5_benbelgacem_bassem/venv/bin/python
# coding: utf-8
"""Module to load data from open food facts into user database"""

from project_5.dbsetter import dbbuilder


def main():
    """Principal application entry point"""
    dbbuilder.build()


if __name__ == "__main__":
    main()
