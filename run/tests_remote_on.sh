#!/bin/bash

env -S "remote_url=$1" pytest tests -n auto --alluredir=reports "${@:2}"