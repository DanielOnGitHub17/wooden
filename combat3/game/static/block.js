class Block{
    constructor(kind){
        // kind: 0 is blank, 1 is wood, 2 is iron
        this.kind = kind;
        Block.blocks[kind].push(this);
        this.build();
    };
    
    build(){
        this.block = add(make(), Game.world);
        this.block.className = `block ${Block.backgrounds[this.kind]}`;
        this.block.object = this;
    };
    static blocks = [[], [], []];
    static backgrounds = ["blank", "wood", "iron"];
    static dimension = 50;
}