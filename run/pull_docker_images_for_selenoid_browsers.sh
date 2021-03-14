#!/bin/bash

awk -F'"' '$0 ~ /selenoid/ {print $4}' etc/selenoid/browsers.json | while read -r image ; do docker pull "$image" ; done
#   |                                  |
#   use " as column separator          |
#          each line in a file---------this file (browsers.json)
#             if matches selenoid in text
#                           print 4th column
#                                                                 pipe everything to next command (docker pull)
#                                                                 where everything are images parsed in previous step