#!/bin/bash


sendMessage() {
    test -z "$1" || api.sendMessage $LOG_CHANNEL_ID "$1"
}

replyLastMessage() {
    test -z "$1" || raw.getLastMessage reply "$1"
}

editLastMessage() {
    test -z "$1" || raw.getLastMessage edit "$1"
}

deleteLastMessage() {
    raw.getLastMessage delete
}

deleteMessages() {
    raw.getMessageCount
    local count=$(($?))
    for ((i=0; i<$count; i++)); do
        deleteLastMessage
    done
}

printMessages() {
    for msg in $(raw.getAllMessages); do
        printf "{%s: %s}\n" $msg "$($msg.print)"
    done
}
