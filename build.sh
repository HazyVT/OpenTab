#!/bin/bash
pyinstaller --add-data "templates:templates" --add-data "static:static"  main.py