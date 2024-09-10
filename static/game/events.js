import { makeEvents, compileMessages } from "../scripts.js";
import { Game } from "./game.js";
import { Gamer } from "./gamer.js";
import { createGameSocket } from "./socket.js";
import { Sound } from "./sound.js";

function main(event) {
    makeEvents({
        load: [start, compileMessages, Sound.load],
        click: [initialize],
        submit: [submitStartForm],
        unload: [leftPage],
        beforeunload: [reloadingPage],
        // fullscreenchange: [gameMode]
    });
    ["open", "close", "message", "error"].forEach(event=>window[event+"Socket"] = eval(event+"Socket"));
}

function gameMode(event, next="WORLD", changeScreen=true) {
    Sound.stopAll();
    INITIALIZER.next = next;
    if (changeScreen) switchScreen("INITIALIZER");
}

function initialize(event) {
    if (event.target != INITIALIZE) return;
    if (!Sound.loaded) Sound.load();
    document.body.requestFullscreen().catch(load);
    Sound.loop(INITIALIZER.next == "SETTINGS" ? "waiting_music" : "game_music");
    switchScreen(INITIALIZER.next);
    INITIALIZER.next = "SETTINGS";
}

function submitStartForm(event) {
    if (Game.isMultiplayer) return;
    event.preventDefault();
    if(event.target == PRACTICE) {
        let prac = PRACTICE.elements;
        Game.game = new Game(+prac.botCount.value+1, +prac.maxHits.value);
        Game.game.start();
    }
}

function events(){
    ["blur", "focus"].forEach((type, i)=>{
        window.addEventListener(type, ()=>{
            Gamer.user.present = i;
            Game.socket.sendGamer(["present"]);
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
    switchScreen("INITIALIZER");
    INITIALIZER.next = "SETTINGS";
    MESSAGES.style.display = "";
    loader();
    if (Game.isMultiplayer) {
        Gamer.load();
        createGameSocket();
        if (Game.rawMaterial.grid && Game.rawMaterial.positions) {  // start immediately - Game is ongoing.
            Game.socket.start(Game.rawMaterial);
        }
        return;
    }
    // switchScreen("GAME_OVER");
}

function messageSocket (event){
    // console.log(event, event.data);
    let data = jsonObj(event.data);
    Game.socket[data.handler](data.data);
};

function closeSocket (event) {
    console.log("Game socket closed. Reforming connection...");
    // create another one
    createGameSocket();
};

function openSocket(event){
    console.log("Connection established with channels");
    // Tell everyone I am here...
    Game.socket.sendGamer();
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

export { gameMode }
