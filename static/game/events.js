addEventListener("submit", (event)=>{
    event.preventDefault();
    if(event.target == PRACTICE) {
        let prac = PRACTICE.elements;
        game = new Game(+prac[0].value, +prac[1].value);
        game.start();
    }
})


onload = ()=>{
    switchScreen("SETTINGS");
    if (Game.isMultiplayer) Gamer.load();
    document.body.onclick = (event)=>{
        event.target == document.body && document.body.requestFullscreen();
    };
    // switchScreen("GAME_OVER");
}

oncontextmenu=(event)=>{
    event.preventDefault()
}

onbeforeunload=(event)=>{
    return false
}