. titanub/utils.sh
. titanub/checks.sh

trap handleSigTerm TERM
trap handleSigInt INT

initNaruto() {
    printLogo
    assertPrerequisites
    sendMessage "Initializing titan..."
    assertEnvironment
    editLastMessage "Starting Titan ..."
    printLine
}

startNaruto() {
    runPythonModule naruto "$@"
}

stopNaruto() {
    sendMessage "Exiting Titan ..."
    exit 0
}

handleSigTerm() {
    log "Exiting With SIGTERM (143) ..."
    stopNaruto
    endLogBotPolling
    exit 143
}

handleSigInt() {
    log "Exiting With SIGINT (130) ..."
    stopNaruto
    endLogBotPolling
    exit 130
}

runNaruto() {
    initNaruto
    startLogBotPolling
    startNaruto "$@"
    stopNaruto
}
