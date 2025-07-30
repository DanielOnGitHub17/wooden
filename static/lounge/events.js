import { makeEvents } from "../scripts.js";

function main() {
    if (!get("CREATEGAME ")) return;
    makeEvents({
        load: [changeBounds, changeCountLabel]
    })
}
// Changing min and max
function changeBounds(event){
    window.gameForm = CREATEGAME.elements;
    gameForm.no_of_players.min = gameForm.wood_strength.min = 2;
    gameForm.no_of_players.max = gameForm.wood_strength.max = 7;
}

// Changing "No_of_players" label
function changeCountLabel(event){
    getS(`[for="id_count"]`).textContent = "Number of Players: ";
}


// Games are created in the server only when it is multiplayer.
onblur=onchange=oninput=(event)=>{
    let target = event.target
    , n = +target.value;
    // For the game creation form - to prevent unbearable changes. Will be repeated in the backend soon.
    switch (event.target.name){
        case "no_of_players":
            gameForm.wood_strength.min = n;
            break;
    }
}

main();