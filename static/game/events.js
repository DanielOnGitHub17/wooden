import { makeEvents, compileMessages } from "../scripts.js";

function main(event) {
    makeEvents({
        load: [start, compileMessages, Sound.load],
        submit: [submitStartForm],
        unload: [leftPage],
        beforeunload: [reloadingPage]
    });
    ["open", "close", "message", "error"].forEach(event=>window[event+"Socket"] = eval(event+"Socket"));
}


function submitStartForm(event) {
    if (Game.isMultiplayer) return;
    event.preventDefault();
    if(event.target == PRACTICE) {
        let prac = PRACTICE.elements;
        window.game = new Game(+prac.botCount.value+1, +prac.maxHits.value);
        game.start();
    }
}

function events(){
    ["blur", "focus"].forEach((type, i)=>{
        window.addEventListener(type, ()=>{
            Gamer.user.present = i;
            gameSocket.sendGamer(["present"]);
        });
    });
}

function leftPage(event) {
    // Delete Gamer - no more in the game.
    `
    or maybe not. The user might have made a mistake -
    `
}

function reloadingPage(event) {
    return false;
}


function start(event){
    switchScreen("SETTINGS");
    MESSAGES.style.display = "";
    loader();
    if (Game.isMultiplayer) {
        Gamer.load();
        createGameSocket();
        if (Game.rawMaterial.grid && Game.rawMaterial.positions) {  // start immediately - Game is ongoing.
            gameSocket.start(Game.rawMaterial);
        }
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
    events();
};

function errorSocket(event) {
    event.preventDefault();
    // event.target.close();
}

function preventRightClick(event){
    event.preventDefault();
}

main();