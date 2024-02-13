class Player{
    constructor(ground){
        this.ground = ground;
        this.build();
    }
    
    build(){
        this.body = add(make(), this.ground);
    }
    move(dir){
        // up: 0, right: 1, down: 2, left: 3
        // moves by navigating through blocks
        // given the direction. it adds
        let next = [];
        for (let i=0; i<2; i++){
            next[i] = this.ground.position[i] + move[dir][i];
        }
        let potentialGround = game.blocks.get(...next);
        if (!potentialGround){
            this.ground = potentialGround;
            this.ground.append(this.body);
        }
    }

    event(){
        window.addEventListener("keyup", (event)=>{
            if (event.key in Player.controls){
                this.move(Player.controls.indexOf(event.key));
            }
        })
    }
    static moves = [[-1, 0], [0, 1], [1, 0], [0, -1]];
    static controls = ["ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft"];
}

// for the other players, the movement updating should be by setInterval
// getting the key of that database in the game to get it's position