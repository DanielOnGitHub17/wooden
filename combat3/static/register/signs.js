function handleMessage(){
    history.replaceState (1, "Normal Location", location.href.split('?')[0])
}

alert()

function doAll(){
    handleMessage()
}
doAll()