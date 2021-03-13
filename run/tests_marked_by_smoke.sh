#!/bin/bash

pytest tests -n auto --alluredir=reports -m smoke "${@:1}"