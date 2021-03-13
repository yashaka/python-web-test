#!/bin/bash

pkill -f allure
pytest tests -n auto --alluredir=reports "${@:1}"
allure serve reports &