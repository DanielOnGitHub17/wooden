// Changing min and max
function changeBounds(event){
    gameForm = CREATEGAME.elements;
    gameForm.count.min = gameForm.max_hits.min = 2;
    gameForm.count.max = gameForm.max_hits.max = 7;
}

for (let handler of [changeBounds]) {
    addEventListener("load", handler)
};

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
