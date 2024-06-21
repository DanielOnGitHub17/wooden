addEventListener("submit", (event)=>{
    event.preventDefault();
    event.target == PRACTICE && (game = new Game(...new FormData(PRACTICE).values().map(i=>+i))).start();
})


onload = ()=>{
    switchScreen("SETTINGS");
    // switchScreen("GAME_OVER");
}

oncontextmenu=(event)=>{
    event.preventDefault()
}

onbeforeunload=(event)=>{
    return false
}