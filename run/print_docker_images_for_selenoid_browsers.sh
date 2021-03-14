#!/bin/bash

awk -F'"' '$0 ~ /selenoid/ {print $4}' etc/selenoid/browsers.json
#   |                                  |
#   use " as column separator          |
#          each line in a file---------this file (browsers.json)
#             if matches selenoid in text
#                           print 4th column
#
# NOTES
# - read more on awk at https://dev.to/rrampage/awk---a-useful-little-language-2fhf