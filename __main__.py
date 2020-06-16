#! P5_benbelgacem_bassem/venv/bin/python
# coding: utf-8
"""Module to launch the application"""

from application import Application


def main():
    """Principal application entry point"""
    app = Application()
    app.start_menu()


if __name__ == "__main__":
    main()
