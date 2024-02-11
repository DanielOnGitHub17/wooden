function handleMessage(){
    history.replaceState (1, "Normal Location", location.split('?')[0])
}
function doAll(){
    handleMessage()
}
doAll()