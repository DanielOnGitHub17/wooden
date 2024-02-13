// world.innerHTML = ''
class Game{
    constructor(hits){
        this.hitsToBreak = hits;
        this.gameRawMaterial = [...Game.world.children].map(i=>JSON.parse(i.textContent))
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

    createPlayer(){
        // choose a ra
        let n = Block.blocks.length;
        new Player(Block.blocks[0][randInt(1, n)]);
    }

    start(){
        this.createPlayer();
    }
    static world = get('world');
}
let game = new Game(10);
game.start();