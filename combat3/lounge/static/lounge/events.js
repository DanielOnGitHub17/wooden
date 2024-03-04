onload = () =>{
    // clear url
    history.replaceState (1, "Normal Location", location.href.split('?')[0]);
    // if nothing in games to join, say so.
    if (!get("gamesToJoin").innerHTML){
        get("gamesToJoin").innerHTML = "No games available. Try creating one below.";
    }
    // and other thins
}
onchange=(event)=>{
    n = +event.target.value
    switch (event.target.id){
        case "nTotal":
            get("maxHits").min = (get("nBots").max = n-1)+2
            break
        
        case "nBots":
            event.target.nextSibling.textContent = ` bot${'s'.repeat(n!=1)} `;
            break
        
        case "maxHits":
            event.target.nextSibling.textContent = ` maximum hit${'s'.repeat(n!=1)} `;
            break
    }
}