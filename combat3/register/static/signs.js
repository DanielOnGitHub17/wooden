function handleMessage(){
    history.replaceState (1, "Normal Location", location.href.split('?')[0])
}

function removeFullname(){
    if (location.href.includes("in")){
        document.forms.querySelector("input").remove()
    }
}
function doAll(){
    handleMessage()
}
doAll()