#!/bin/bash

pytest tests -n auto --alluredir=reports -m "$1" "${@:2}"