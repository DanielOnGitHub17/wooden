class Block{
    constructor(kind){
        // kind: 0 is sand, 1 is wood, 2 is iron
        this.kind = kind;
        Block.blocks[kind].push(this);
        this.build();
    };
    
    build(){
        this.block = add(make(), Game.world);
        this.block.className = `block ${Block.backgrounds[this.kind]}`;
        this.block.object = this;
    };

    crack(){
        if (this.kind != 1) return;
        // remove from initial kind, then add to space
        let [r, c] = this.position;
        // fetch(`/game/crack?r=${r}&c=${c}`)
        transfer(this, Block.blocks[1], Block.blocks[0]);
        game.grid[r][c] = 0;
        this.kind = 0;
        this.block.className = 'block sand';
        if (!Block.blocks[1].length){
            game.end();
        }
    }
    static blocks = [[], [], []];
    static backgrounds = ["sand", "wood", "iron"];
    static dimension = 50;
}