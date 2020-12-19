declare -r minPVer=8
declare -r maxPVer=10

getPythonVersion() {
    local -i count=$minPVer
    local tmp
    while true; do
        tmp=$(python3.$count -V 2> /dev/null)
        [[ -n $tmp || $count -gt $maxPVer ]] && break
        count+=1
    done
    declare -gr pVer=$(sed -E 's/Python (3\.[0-9]{1,2}\.[0-9]{1,2}).*/\1/g' <<< $tmp)
}

log() {
    local text="$*"
    test ${#text} -gt 0 && test ${text::1} != '~' \
        && echo -e "[$(date +'%d-%b-%y %H:%M:%S') - INFO] - titanub - ${text#\~}"
}

quit() {
    local err="\t:: ERROR :: $1\nExiting With SIGTERM (143) ..."
    if (( getMessageCount )); then
        replyLastMessage "$err"
    else
        log "$err"
    fi
    exit 143
