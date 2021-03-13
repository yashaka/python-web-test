#!/bin/bash

pytest tests -n $1 --alluredir=reports "${@:2}"