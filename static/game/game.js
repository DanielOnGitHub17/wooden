identify()
class Game{
    constructor(count, hits){
        [this.hits, this.count] = [hits, count+1];
        this.grid = copyObj(Game.rawMaterial.grid);
        Game.isMultiplayer || this.build_grid();
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
        // There should be a kind of loading now ...
        setTimeout(()=>{
            this.setPositions();
        }, 500)
    }
    setPositions(){
        // If positions is a dict, the game is multiplayer, else, it is one person. 
        // Chec
        this.positions = copyObj(Game.rawMaterial.positions).slice(0, this.count);
        let forPlayer = Game.isMultiplayer ? Game.player : 0
        , playerPos = this.positions[forPlayer];

        new Player(this.blocks[playerPos[0]][playerPos[1]], forPlayer);
        delete this.positions[forPlayer];
        
        for (let name in this.positions){
            let pos = this.positions[name];
            new Bot(this.blocks[pos[0]][pos[1]], name);
        }
    }
    end(){
        // with button to 'save game' -> Maybe get the path you took... (for multiplayer only)
        // location = `/game/end?GAME=${get("site").textContent}`
        switchScreen("GAME_OVER");
        this.listWinners();
    }
    listWinners(){
        // sort winners (maybe by brute force)
        let winners = Bot.bots.concat(Player.players).sort((a, b)=>b.blocksBroken - a.blocksBroken)
        , winnersPush = setInterval(() => {
            let winner = winners.pop();
            WINNERS_LIST.insertBefore(make("li"), WINNERS_LIST.firstElementChild).textContent = `${winner.name}. Score: ${winner.blocksBroken}`;
            if (!winners.length) clearInterval(winnersPush);
        }, 1000);
    }

    static world = WORLD;
    static player = 0
    static isMultiplayer = Boolean(get("WAIT_ROOM"))
    static rawMaterial = Game.isMultiplayer ? {"grid":[], "positions":{}} : jsonObj(GAME_DATA.textContent);
}
// let game = new Game(...getAll("#gameInfo>span").map(info=>+info.textContent))

// setTimeout(()=>game.start(), 3000) // should say three two one.