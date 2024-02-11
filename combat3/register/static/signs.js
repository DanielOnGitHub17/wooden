function handleMessage(){
    history.replaceState (1, "Normal Location", location.href.split('?')[0])
}

function removeFullname(){
    if (location.href.includes("in")){
        document.forms[0].querySelector("[name=fullname]").parentElement.remove()
    }
}
function doAll(){
    handleMessage()
    removeFullname()
}
doAll()