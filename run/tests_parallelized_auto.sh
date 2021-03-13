#!/bin/bash

pytest tests -n auto --alluredir=reports "${@:1}"