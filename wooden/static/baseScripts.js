let registerLinks = get("registerLinks")
showRegister.addEventListener("focus", (event)=>{
    event.stopPropagation();
    registerLinks.className = "visible";
})


showRegister.addEventListener("blur", (event)=>{
    event.stopPropagation();
    setTimeout(()=>registerLinks.className = "", 400);
})