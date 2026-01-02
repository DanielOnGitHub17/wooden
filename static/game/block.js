import { Game } from "./game.js";
import { Sound } from "./sound.js";

class Block {
    constructor(kind) {
        // kind: 0 is sand, 1 is wood, 2 is iron
        this.kind = kind;
        Block.blocks[kind].push(this);
        this.build();
    };

    build() {
        this.block = add(make(), Game.world);
        this.block.className = `block ${Block.backgrounds[this.kind]}`;
        this.block.object = this;
    };

    crack() {
        if (this.kind != 1) return;
        Sound.play("wood_break");
        // remove from initial kind, then add to space
        let [r, c] = this.position;
        transfer(this, Block.blocks[1], Block.blocks[0]);
        Game.game.grid[r][c] = 0;
        this.kind = 0;
        this.block.className = 'block sand';
        if (!Block.blocks[1].length) {
            Game.game.end();
        }
    }
    static blocks = [[], [], []];
    static backgrounds = ["sand", "wood", "iron"];
    static dimension = 50;
}

export { Block }
