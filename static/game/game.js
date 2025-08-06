import { gameMode } from "./events.js";
import { Player } from "./player.js";
import { Bot } from "./bot.js";
import { Block } from "./block.js";
import { Gamer } from "./gamer.js";
import { Sound } from "./sound.js";

identify()
class Game{
    constructor(numberOfPlayers, hits){
        [this.numberOfPlayers, this.hits] = [numberOfPlayers, hits];
        this.grid = copyObj(Game.rawMaterial.grid);
        this.build_grid();
        Game.isMultiplayer && this.setPositions();
        // Game.world.style.width = Game.world.style.height = this.length*Block.dimension + 'px';
    }
    build_grid(){
        this.blocks = []
        this.grid.forEach((textureLine, r)=>{
            this.blocks.push([]);
            textureLine.forEach((kind, c) => {
                this.blocks[r].push(new Block(kind));
                this.blocks[r][c].position = [r, c];
            });
        });
        this.blocks.get = (r, c) => this.blocks[r][c];
    }
    start(){
        switchScreen("WORLD");
        if (Game.isMultiplayer){
            // Associate Gamers with Players
            Bot.bots.concat(Player.players).forEach(obj=>Gamer.gamers[obj.name].player = obj);
            // Get time for timeout
            let startIn = 1000*Game.rawMaterial.time - Date.parse(new Date());
            showLoading(`Starting in ${parseInt(startIn/1000)} seconds`);
            console.log(startIn);
            // approximate - for when user refreshes and game has started.
            if (startIn < -1000){
                gameMode();
            }
            setTimeout(() => {
                Gamer.user.player.event();  // Start accepting input.
                hideLoading();
            }, startIn);
            return;
        }
        showLoading("Starting soon...");
        Sound.stopAll();
        Sound.loop("game_music");
        setTimeout(()=>{
            this.setPositions();  // could be animated...
            hideLoading();
        }, 3000)
    }
    setPositions(){
        // If positions is a dict, the game is multiplayer, else, it is one person.
        
        let forPlayer = Game.player;
        this.positions = copyObj(Game.rawMaterial.positions);
        if (!Game.isMultiplayer){
            this.positions = this.positions.slice(0, this.numberOfPlayers);
        }
        let playerPos = this.positions[forPlayer];
        new Player(this.blocks[playerPos[0]][playerPos[1]], forPlayer);
        delete this.positions[forPlayer];
        
        for (let name in this.positions){
            let pos = this.positions[name];
            new Bot(this.blocks[pos[0]][pos[1]], name);
        }
    }
    end(){
        Sound.stopAll();
        // with button to 'save game' -> Maybe get the path you took... (for multiplayer only)
        switchScreen("GAME_OVER");
        // setTimeout to fix bug. Bug: When players' scores are too close, lower might appear upper than higher.
        setTimeout(()=>this.listWinners(), 500);
        WINNERS_LIST.textContent = "Compiling winners...";
    }
    listWinners(){
        WINNERS_LIST.textContent = "";
        // Sort winners by descending order of blocksBroken
        let winners = Bot.bots.concat(Player.players).sort((a, b)=>b.blocksBroken - a.blocksBroken)
        , winScore = winners[0].blocksBroken
        , winnersPush = setInterval(() => {
            Sound.play("pile_player");
            let winner = winners.pop();
            WINNERS_LIST.insertBefore(make("li"), WINNERS_LIST.firstElementChild).textContent = `${winner.name}. Score: ${winner.blocksBroken}`;
            if (!winners.length) {
                setTimeout(()=>Sound.loop("waiting_music"), 200);
                clearInterval(winnersPush);
                Game.isMultiplayer && this.sendStatus(Gamer.user.player.blocksBroken >= winScore);
            };
        }, 1000);
    }

    sendStatus(won){
        SEND_STATUS.elements.won.checked = won;
        STATUS.textContent = won ? "CONGRATULATIONS!!! You won the game!" 
        : "Sorry, you did not win. Break more wood next time.";
    }

    static world = WORLD;
    static player = 0;
    static isMultiplayer = Boolean(get("WAIT_ROOM"));
    static rawMaterial = jsonObj(GAME_DATA.textContent);
}

export { Game }
