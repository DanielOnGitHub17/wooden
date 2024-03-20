class Player{
    constructor(ground, name){
        Player.players.push(this);
        this.name = name;
        this.ground = ground;
        this.hits = 0;
        this.blocksBroken = 0;
        this.next = ground.position;
        this.name = name
        this.build();
        this.event();
    }
    
    build(){
        this.body = add(make(), this.ground.block);
        this.body.className = "player";
        this.body.object = this;
    }

    nextGround(dir){
        let next = [];
        for (let i=0; i<2; i++){
            next[i] = this.ground.position[i] + Player.moves[dir][i];
        }
        return [game.blocks.get(...next), next];
    }

    move(dir){
        // up: 0, right: 1, down: 2, left: 3
        // first it looks towards where it wants to go
        this.body.style.transform = `rotate(${dir*90}deg`;
        // moves by navigating through blocks
        // given the direction. it adds
        let [potentialGround, next] = this.nextGround(dir);
        if (potentialGround.kind != 1){
            this.hits = 0; // it turned away from a wood block.
            if (!potentialGround.kind){ // sand (change position)
                this.ground = potentialGround;
                this.ground.block.append(this.body);
                // time to learn about websockets in JS
                // and, apparently, Django channels
            }
        } else {// wood
            // if it hits the block ten times, the block breaks
            if (JSON.stringify(this.next) == JSON.stringify(next)){ // checks if it's still hitting the same wooden block
                this.hits += 1;
                if (this.hits >= game.hitsToBreak){ // the > is unneccesary
                    this.hits = 0;
                    potentialGround.crack();
                    this.blocksBroken += 1;
                    if (this.name == Game.player) this.setScore()
                    // tell server that a block has broken with the blocks r,c
                    // will be the one sent
                    // thank you God for helping me fix the 'who broke it'.
                    // all players will have scores attributed to them
                    // if their JavaScript says they broke it.
                    // which means that, if there is a clash, both teams get a point.
                }
            } else{
                // set the hits to one because it just started hitting this one
                this.hits = 1;
                // now, set it to make this it's next
                this.next = potentialGround.position;
            }
        }
        return potentialGround.kind;
    }

    event(){
        window.addEventListener("keyup", (event)=>{
            event.preventDefault();
            if (Player.controls.includes(event.key)){
                this.move(Player.controls.indexOf(event.key));
            }
        })
    }

    data(){
        // return [] every useful thing of this player
    }

    send(){
        // send this.data() to server
    }

    setScore(){
        fetch(`/game/score?score=${this.blocksBroken}`)
    }

    static moves = [[-1, 0], [0, 1], [1, 0], [0, -1]];
    static controls = ["ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft"];
    static players = [];
}

// for the other players, the movement updating should be by setInterval
// getting the key of that database in the game to get it's position
// instead of shooting, the game could be who broke the most number of blocks, better (i think)

// Block cracking
// algorithm for left right could check next element and previous element... 
// if a 'path' is defined, algorithm could walk through that path (which would mean that broken blocks will
// be added to a specific position in the path. (if the path contBotns only sand))
// if the path is of all blocks, movement will move till it reaches sand.
// I think the present algorithm is okay.

// moveRight = () =>{
//     return new KeyboardEvent("keyup", {
//         key: "ArrowRight"
//     })
// }
// later, implement Bot movement that will move right... down... left. till it reaches the end
// and breaks all blocks
// remember that game.js should put the players in actual positions given to them by the server
// not just random.

// dispatchEvent(new KeyboardEvent("keyup", {
//     key: Player.controls[dir]
//     , stopPropagation: true
// }));


// style blocks according to number of breaks friendly blocks to hard ones
// blocks change on hit to other type
// wood.strength