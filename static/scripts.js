identify();

function main() {
    let cheat = [];
    if (window.CHEATS){
        CHEATS.style.display = "none";
        cheat.push(showCheats);
    }
    let events = {
        load: [changeNavStyle, compileMessages]
        , click: [makeMenu]
        , keyup: cheat
    }

    for (let type in events){
        for (let handler of events[type]){
            window.addEventListener(type, handler);
        }
    }
}

function makeMenu(event) {
    if (event.target == SHOW_MENU){
        [[MENU, "show"], [APP, "blur"]].forEach(each=>{reclass(...each, hasClass(...each))});
    }
}

function changeNavStyle(event) {
    const navLink = getS(`nav [href='${location.pathname}']`);
    if (navLink ) navLink.className = 'nav-sign-up';
}

function compileMessages(event){
    getAll(".errorlist").forEach(list=>{
        console.log(list)
        list.remove();
        ERRORS.append(list);
    });
    reclass(MESSAGES, MESSAGES.textContent.trim() == 'X' ? "empty" : "show");
}

function forceFullScreen(event){
    switchScreen("START");
    document.addEventListener("fullscreenchange", (event)=>{
        switchScreen(document.fullscreenElement == document.firstElementChild ? "APP" : "START")
    })
}


function showCheats(event){
    if (event.ctrlKey && event.shiftKey && event.altKey && event.key == 'C'){
       CHEATS.style.display = "";
    }
}

main()