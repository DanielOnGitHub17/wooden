class Gamer{
    constructor(username, joined=false, present=false){
        [this.username, this.joined, this.present] = arguments;
        Gamer.gamers[username] = this;
        this.build();
        Object.defineProperties(this, {
            "joined": {
                set: (bool)=>this.joinedCheck.checked = bool,
                get: ()=>this.joinedCheck.checked
            },
            "present": {
                set: (bool)=>this.presentCheck.checked = bool,
                get: ()=>this.presentCheck.checked
            }
        })
    }

    build(){
        // PLAYERS_LIST
        (this.nameBox = (this.row = PLAYERS_LIST.insertRow()).insertCell()).textContent = this.username;
        ["joined", "present"].forEach(prop => {
            add(this[prop+"Check"] = make("input"), this.row.insertCell()).type = "checkBox";
            this[prop+"Check"].checked = this[prop];
            this[prop+"Check"].disabled = true;
        });
    }

    leave(){
        this.row.remove();
        delete Gamer[this.username];
        this.player && this.player.remove();
    }
    
    static load(){
        for (let username in Gamer.gamersData){
            new Gamer(username, ...Gamer.gamersData[username]);
        }
    }
    static get user(){
        return Gamer.gamers[Gamer.username];
    }

    static gamers = {};
    static gamersData = jsonObj(GAMERS.textContent);
    static gameID = +ID.textContent;
    static username = USERNAME.textContent;
    static N = +N.textContent;
    static creator = Boolean(get("CREATOR"));
}