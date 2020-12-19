#!/bin/bash


declare -r _api_url="https://api.telegram.org/bot"
declare -i _mid=0
declare -a _allMessages=()

_getResponse() {
    if [[ -n $BOT_TOKEN && -n $LOG_CHANNEL_ID ]]; then
        local reqType=${1#api.} parse=false; shift
        test ${reqType::4} = "send" && parse=true
        local params=$(sed 's/ /\&/g' <<< $*)
        test -n $params && params="?$params"
        local rawUpdate=$(curl -s ${_api_url}${BOT_TOKEN}/${reqType}${params})
        local ok=$(echo $rawUpdate | jq .ok)
        test -z $ok && return 1
        if test $ok = true; then
            if test $parse = true; then
                local msg="msg$_mid"
                Message $msg
                $msg.parse $_mid "$rawUpdate"
                _allMessages[$_mid]=$msg
                let _mid+=1
            fi
        else
            local errcode=$(echo $rawUpdate | jq .error_code)
            local desc=$(echo $rawUpdate | jq .description)
            quit "invalid request ! (caused by core.api.$FUNCNAME)
\terror_code : [$errcode]
\tdescription : $desc"
        fi
        sleep 0.6
    fi
}
