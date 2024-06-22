class Gamer{
    constructor(username, joined, present){
        [this.username, this.joined, this.present] = arguments;
        Gamer.gamers[username] = this;
        this.build();
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

    static load(){
        for (let username in Gamer.gamersData){
            new Gamer(username, ...Gamer.gamersData[username]);
        }
    }
    static gamers = {};
    static gamersData = jsonObj(GAMERS.textContent);
}