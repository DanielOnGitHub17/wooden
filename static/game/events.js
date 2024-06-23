addEventListener("submit", (event)=>{
    event.preventDefault();
    if(event.target == PRACTICE) {
        let prac = PRACTICE.elements;
        game = new Game(+prac[0].value, +prac[1].value);
        game.start();
    }
});

events = ()=>{
    ["blur", "focus"].forEach((type, i)=>{
        window.addEventListener(type, ()=>{
            Gamer.user.present = i;
            gameSocket.sendGamer(["present"]);
        });
    });
}

window.addEventListener("unload", (event)=>{
    // Delete Gamer - no more in the game.
    `
    or maybe not. The user might have made a mistake -
    `
})
window.addEventListener("beforeunload", (event)=>{
    return false;
});

onload = ()=>{
    switchScreen("SETTINGS");
    loader();
    if (Game.isMultiplayer) {
        Gamer.load();
        createGameSocket();
        events();
        return
    }
    // switchScreen("GAME_OVER");
}

function messageSocket (event){
    // console.log(event, event.data);
    let data = jsonObj(event.data);
    gameSocket[data.handler](data.data);
};

function closeSocket (event) {
    console.log("Game socket closed. Reforming connection...");
    // create another one
    createGameSocket();
};

function openSocket(event){
    console.log("Connection established with channels");
    // Tell everyone I am here...
    gameSocket.sendGamer();
};

function errorSocket(event) {
    event.preventDefault();
    // event.target.close();
}

oncontextmenu=(event)=>{
    event.preventDefault();
}
