function createGameSocket() {
    delete gameSocket;  // Hopefully I won't be deleting the real gameSocket often
    if (window.gameSocket) {
        while (gameSocket.CONNECTING) {}
    }
    gameSocket = new GameSocket();
    ["open", "close", "message", "error"].forEach(
        event=>gameSocket.addEventListener(event, window[event+"Socket"])
    );
}

class GameSocket extends WebSocket{
    constructor(){
        super(`ws${(location.protocol=="https:")?'s':''}://${location.host}/ws/game/${Gamer.gameID}/`);
    }

    start(data){
        Game.player = Gamer.username;
        for (let prop in data){
            Game.rawMaterial[prop] = data[prop];
        };
        window.game = new Game(Object.values(data.positions).length, data.hits);
        game.start();
    }

    move(dir){
        this.send(jsonStr({
            handler: "playerMove", data: {username: Gamer.username, dir: dir}
        }));
    }

    playerMove(data){
        Gamer.gamers[data.username].player.move(data.dir);
    }

    createGamer(username){
        // When someone joins the game but is still in their lounge page
        new Gamer(username);
    }

    playerUpdate(data){
        let gamer = Gamer.gamers[data.username];
        for (let prop in data) gamer[prop] = data[prop];
        if (data["joined"]){
            COUNT.textContent = getAll("#PLAYERS_LIST td:nth-child(2)>input").filter(i=>i.checked).length;
        }
        // Disable leave button/start button.
        this.disenableForms(+COUNT.textContent);
    }

    playerLeave(username){
        this.disenableForms(COUNT.textContent = +COUNT.textContent-1);
        let gamer = Gamer.gamers[username];
        gamer && gamer.leave();
    }

    sendGamer(props=["joined", "present"]){
        let gamer = Gamer.gamers[Gamer.username], obj = {};
        ["username"].concat(props).forEach(prop => obj[prop] = gamer[prop]);
        this.send(jsonStr({handler: "playerUpdate", data: obj}));
    }

    disenableForms(count){
        GAME_STARTER.disabled = count < 2;
        if (Gamer.creator){
            GAME_LEAVER.disabled = count > 1;
        }
    }
}