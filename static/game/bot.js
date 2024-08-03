class Bot extends Player{
    constructor(ground, name){
        super(ground, name);
        // this.name.length < 3 && "Bot "+this.name || this.name (Just playing.)
        if (name.length < 3) this.name = "Bot "+name;  // Normal users must have usernames greater than three chars anyway!
        this.moving = false;
        this.dirs = [];
        this.moveMethod();
        transfer(this, Player.players, Bot.bots);
        this.body.className += " bot";
        // Imagine making the game big to take millions of players playing at the same time.
        // Maybe a story/ an endless mode, blocks will be around the city, you just go to break
        // Real people only (maybe bots too), it will be nice to just go and see a character
        // And two of you might even chat and decide to clear a place/build a pattern (having build will be cool)
    }
    moveMethod(){
        if (!Game.isMultiplayer){
            moveBy = `move${choice(Bot.moveBy)}`;
            console.log(moveBy)
            this.movInterval = setInterval(()=>{
                this[moveBy]();
            }, 200);
            return;
        }
    }
    moveSpiral(){
        // turning algorithm
    }
    moveLinear(){
        // up to down algorithm
    }
    event(){}
    moveRandom(){
        // 'random' algorithm (chooses a random block and goes to break it
        //, breaking obstacles along the way, of course)
        if (this.moving){
            if (this.ground.position[0] != this.randomWood[0]){
                this.move(this.dirs[0])
            } else if (this.ground.position[1] != this.randomWood[1]){
                this.move(this.dirs[1])
            }else{
                this.moving = false
            }
        } else{
            this.moving = true;
            try{
                this.randomWood = choice(Block.blocks[1]).position;
            } catch (error){
                clearInterval(this.movInterval);
                this.moving = false;
                return;
            }
            // 0,2 for up/down.
            this.dirs[0] = 2*(this.randomWood[0] >= this.ground.position[0])
            // 1/3 for right/left
            this.dirs[1] =  1 + 2*(this.ground.position[1] >= this.randomWood[1]);
        }
    }
    static bots = [];
    static moveBy = ["Random"]; // "Spiral", "Linear", "BFS", "DFS", ...
}
