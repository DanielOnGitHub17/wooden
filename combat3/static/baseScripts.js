let registerLinks = get("registerLinks")
showRegister.addEventListener("focus", (event)=>{
    event.stopPropagation();
    console.log("Hi");
    registerLinks.className = "visible";
})


showRegister.addEventListener("blur", (event)=>{
    event.stopPropagation();
    console.log("Hi");
    setTimeout(()=>registerLinks.className = "", 400);
})