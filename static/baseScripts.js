identify();
addEventListener("click", (event)=>{
    event.stopPropagation();
    if (event.target.id == "showRegister") {
        console.log("OUCH")
        registerLinks.className = "visible";
    }
})


addEventListener("click", (event)=>{
    if (![showRegister, registerLinks].includes(event.target)) registerLinks.className = "";
})