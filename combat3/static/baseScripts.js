let registerLinks = get("registerLinks")
showRegister.addEventListener("focus", (event)=>{
    event.stopPropagation();
    console.log("Hi");
    registerLinks.className = "visible";
})

addEventListener("blur", (event)=>{
    switch (event.target.id){
        case ("showRegister"):
            console.log("Bye")
            registerLinks.className = ""
            break
    }
})
