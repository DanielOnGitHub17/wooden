function handleMessage(){
    history.replaceState (1, "Normal Location", location.href.split('?')[0])
}

function doAll(){
    handleMessage()
}
doAll()