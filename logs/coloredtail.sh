#!/bin/bash
tail "$@" | awk '
BEGIN {
    BLUE="\033[0;34m"
    RED="\033[0;31m"
    YELLOW="\033[0;33m"
    GREEN="\033[0;32m"
    NOCOLOR="\033[0m"
}

{
    if ($0 ~ /run time:/) {
        $0=gensub(/(run time: )([^,]*)/, "\\1" BLUE "\\2" NOCOLOR, "g")
    }

    if ($0 ~ /executions:/) {
        $0=gensub(/(executions: )([^,]*)/, "\\1" BLUE "\\2" NOCOLOR, "g")
    }

    if ($0 ~ /exec\/sec:/) {
        exec_sec = gensub(/.*exec\/sec: ([0-9]+).*/, "\\1", "g")
        if (exec_sec < 5000) {
            color = RED
        } else if (exec_sec <= 7000) {
            color = YELLOW
        } else {
            color = GREEN
        }
        $0=gensub(/(exec\/sec: )([0-9]+)/, "\\1" color "\\2" NOCOLOR, "g")
    }

    print $0
}'

# this command colours the output of tail, highlighting the regexes. This was made to work with this output:
# [Stats #0] run time: 9h-36m-22s, clients: 1, corpus: 55, objectives: 0, executions: 163983117, exec/sec: 4741
