import { Game } from "./game.js";
import { Gamer } from "./gamer.js";

function createGameSocket() {
    delete Game.socket;  // Hopefully I won't be deleting the real Game.socket often
    if (Game.socket) {
        while (Game.socket.CONNECTING) { }
    }
    Game.socket = new GameSocket();
    ["open", "close", "message", "error"].forEach(
        event => Game.socket.addEventListener(event, window[event + "Socket"])
    );
}

class GameSocket extends WebSocket {
    constructor() {
        super(`ws${(location.protocol == "https:") ? 's' : ''}://${location.host}/ws/game/${Gamer.gameID}/`);
    }

    start(data) {
        Game.player = Gamer.username;
        for (let prop in data) {
            Game.rawMaterial[prop] = data[prop];
        };
        Game.game = new Game(Object.values(data.positions).length, data.hits);
        Game.game.start();
    }

    move(dir) {
        this.send(jsonStr({
            handler: "playerMove", data: { username: Gamer.username, dir: dir }
        }));
    }

    playerMove(data) {
        Gamer.gamers[data.username].player.move(data.dir);
    }

    createGamer(username) {
        // When someone joins the game but is still in their lounge page
        new Gamer(username);
    }

    playerUpdate(data) {
        let gamer = Gamer.gamers[data.username];
        for (let prop in data) gamer[prop] = data[prop];
        if (data["joined"]) {
            NO_OF_PLAYERS.textContent = getAll("#PLAYERS_LIST td:nth-child(2)>input").filter(i => i.checked).length;
        }
        // Disable leave button/start button.
        this.disenableForms(+NO_OF_PLAYERS.textContent);
    }

    playerLeave(username) {
        this.disenableForms(NO_OF_PLAYERS.textContent = +NO_OF_PLAYERS.textContent - 1);
        let gamer = Gamer.gamers[username];
        gamer && gamer.leave();
    }

    sendGamer(props = ["joined", "present"]) {
        let gamer = Gamer.gamers[Gamer.username], obj = {};
        ["username"].concat(props).forEach(prop => obj[prop] = gamer[prop]);
        this.send(jsonStr({ handler: "playerUpdate", data: obj }));
    }

    disenableForms(numberOfPlayers) {
        if (Gamer.creator) {
            GAME_STARTER.disabled = numberOfPlayers < 2;
            GAME_LEAVER.disabled = numberOfPlayers > 1;
        }
    }
}

export { createGameSocket };
