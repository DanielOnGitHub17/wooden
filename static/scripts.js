identify();
// General
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

for (let handler of [changeNavStyle, compileMessages]){
    window.addEventListener("load", handler);
}

// For How To Play
if (window.cheats){
    cheats.style.display = "none";
    window.addEventListener("keyup", (event)=>{
        if (event.ctrlKey && event.shiftKey && event.altKey && event.key == 'C'){
            cheats.style.display = "";
        }
    })
}