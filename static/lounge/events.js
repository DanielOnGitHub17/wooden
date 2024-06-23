onload = () =>{
    // if nothing in games to join, say so.
    IN_GAME = !Boolean(get("gamesToJoin"));
    if (IN_GAME) {
        return
    }
    if (!gamesToJoin.innerHTML.trim()){
        gamesToJoin.innerHTML = "No games available. Try creating one above.";
    }
    gameForm = CREATEGAME.elements;
    gameForm.count.min = gameForm.max_hits.min = 2;
    gameForm.count.max = gameForm.max_hits.max = 7;
}

// Games are created in the server only when it is multiplayer.
onblur=onchange=oninput=(event)=>{
    let target = event.target
    , n = +target.value;
    // For the game creation form - to prevent unbearable changes. Will be repeated in the backend soon.
    switch (event.target.name){
        case "count":
            gameForm.max_hits.min = n;
            break;
    }
}
// "99 // 4 -> 99" (WHY??? - (Python programmer switched to JavaScript))