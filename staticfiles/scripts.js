identify();
// General
function changeNavStyle(event) {
    const navLink = getS(`nav [href='${location.pathname}']`);
    if (navLink ) navLink.className = 'nav-sign-up';
}
window.addEventListener("load", changeNavStyle)

// For How To Play
if (window.cheats){
    cheats.style.display = "none";
    window.addEventListener("keyup", (event)=>{
        if (event.ctrlKey && event.shiftKey && event.altKey && event.key == 'C'){
            cheats.style.display = "";
        }
    })
}