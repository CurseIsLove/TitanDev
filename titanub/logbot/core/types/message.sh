#!/bin/bash


Message() {
    . <(sed "s/_Message/$1/g" titanub/logbot/core/types/messageClass.sh)
}
