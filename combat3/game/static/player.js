class Player{
    constructor(ground){
        Player.players.push(this);
        this.ground = ground;
        this.block = 0;
        this.next = ground.position;
        this.build();
        this.event();
    }
    
    build(){
        this.body = add(make(), this.ground.block);
        this.body.className = "player";
        this.body.object = this;
    }
    move(dir){
        // up: 0, right: 1, down: 2, left: 3
        // first it looks towards where it wants to go
        this.body.style.transform = `rotate(${dir*90}deg`;
        // moves by navigating through blocks
        // given the direction. it adds
        let next = [];
        for (let i=0; i<2; i++){
            next[i] = this.ground.position[i] + Player.moves[dir][i];
        }
        let potentialGround = game.blocks.get(...next);
        if (potentialGround != 1){
            if (!potentialGround.kind){
                this.ground = potentialGround;
                this.ground.block.append(this.body);
        } else {// wood
            // if it hits the block ten times, the block breaks
            if (JSON.stringify(this.next) == JSON.stringify(next)){
                this.bullet += 1;
                if (this.bullet == game.hitsToBreak){
                    this.bullet = 0;
                    potentialGround.crack();
                }
                // set the bullet to zero
                this.bullet = 0;
            } else{
                this.bullet = 0;
            }
        }
    }

    event(){
        window.addEventListener("keyup", (event)=>{
            if (Player.controls.includes(event.key)){
                this.move(Player.controls.indexOf(event.key));
            }
        })
    }
    static moves = [[-1, 0], [0, 1], [1, 0], [0, -1]];
    static controls = ["ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft"];
    static players = [];
}

// for the other players, the movement updating should be by setInterval
// getting the key of that database in the game to get it's position
// instead of shooting, the game could be who broke the most number of blocks, better (i think)