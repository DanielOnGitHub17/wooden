identify();
const username = window.USERNAME ? USERNAME.textContent : "player";

function main(event) {
    let cheat = [];
    if (window.CHEATS){
        CHEATS.style.display = "none";
        cheat.push(showCheats);
    }
    makeEvents({
        load: [changeNavStyle, compileMessages]
        , click: [makeMenu, showOnline, hideOnline]
        , keyup: cheat
    });
}

function makeMenu(event) {
    if (event.target == window.SHOW_MENU){
        [[MENU, "show"], [APP, "blur"]].forEach(each=>{reclass(...each, hasClass(...each))});
        SHOW_MENU.textContent = hasClass(MENU, "show") ? "Close" : "Menu";
    }
}

function showOnline(event){
    if (event.target == window.SHOW_ONLINE){
        reclass(PEOPLE, "show");
    }
}

function hideOnline(event){
    if (event.target == window.HIDE_ONLINE){
        reclass(PEOPLE, "show", true);
    }
}

function changeNavStyle(event) {
    const navLink = getS(`nav [href='${location.pathname}']`);
    if (navLink ) navLink.className = 'nav-sign-up';
}

function compileMessages(event){
    getAll(".errorlist").forEach(list=>{
        list.remove();
        ERRORS.append(list);
    });
    reclass(MESSAGES, MESSAGES.textContent.trim() == 'X' ? "empty" : "show");
}

function forceFullScreen(event){
    switchScreen("START");
    document.addEventListener("fullscreenchange", (event)=>{
        switchScreen(document.fullscreenElement == document.firstElementChild ? "APP" : "START")
    });
}


function showCheats(event){
    if (event.ctrlKey && event.shiftKey && event.altKey && event.key == 'C'){
       CHEATS.style.display = "";
    }
}

function makeEvents(events){
    for (let type in events){
        for (let handler of events[type]){
            window.addEventListener(type, handler);
        }
    }
}

main();

export { makeEvents, username, compileMessages };