#!/bin/bash

pytest tests -n auto --alluredir=reports -m 'not smoke' "${@:1}"