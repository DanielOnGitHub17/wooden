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
        this.kind = 0;
        this.block.className = 'block sand';
    }
    static blocks = [[], [], []];
    static backgrounds = ["sand", "wood", "iron"];
    static dimension = 50;
}