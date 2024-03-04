// world.innerHTML = ''
class Game{
    constructor(hits, real, bots){
        this.hitsToBreak = hits;
        this.gameRawMaterial = JSON.parse(Game.world.innerHTML)
        this.positions = eval(get("positions").textContent)
        Game.world.innerHTML = '';
        this.length = this.gameRawMaterial.length;
        // Game.world.style.width = Game.world.style.height = this.length*Block.dimension + 'px';
        this.blocks = []
        this.gameRawMaterial.forEach((textureLine, r)=>{
            this.blocks.push([]);
            textureLine.forEach((kind, c) => {
                this.blocks[r].push(new Block(kind));
                this.blocks[r][c].position = [r, c];
            });
        });
        this.blocks.get = (r, c) => this.blocks[r][c];
        // Make another reference to blocks
    }
    start(){
        for (let i in this.positions){
            let pos = this.positions[+i]
            if (!(pos[0] == Game.player)){
                new Bot(this.blocks[pos[1]][pos[2]], pos[0])
            } else{
                new Player(this.blocks[pos[1]][pos[2]], pos[0])
            }
        }
    }
    static world = get("world");
    static player = get("username").textContent;
}
let game = new Game(...getAll("#gameInfo>span").slice(1, -1).map(info=>+info.textContent))
game.start();