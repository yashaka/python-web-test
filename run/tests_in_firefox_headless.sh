#!/bin/bash

env -S 'browser_name=firefox headless=True' pytest tests -n auto --alluredir=reports "${@:1}"