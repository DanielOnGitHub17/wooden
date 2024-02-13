class Player{
    constructor(ground){
        Player.players.push(this);
        this.ground = ground;
        this.hits = 0;
        this.blocksBroken = 0;
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
        if (potentialGround.kind != 1){
            this.hits = 0; // it turned away from a wood block.
            if (!potentialGround.kind){ // sand (change position)
                this.ground = potentialGround;
                this.ground.block.append(this.body);
            }
        } else {// wood
            // if it hits the block ten times, the block breaks
            if (JSON.stringify(this.next) == JSON.stringify(next)){ // checks if it's still hitting the same wooden block
                this.hits += 1;
                if (this.hits >= game.hitsToBreak){ // the > is unneccesary
                    this.hits = 0;
                    potentialGround.crack();
                    this.blocksBroken += 1; // will be the one sent
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
// be added to a specific position in the path. (if the path contains only sand))
// if the path is of all blocks, movement will move till it reaches sand.
// I think the present algorithm is okay.

// moveRight = () =>{
//     return new KeyboardEvent("keyup", {
//         key: "ArrowRight"
//     })
// }
// later, implement AI movement that will move right... down... left. till it reaches the end
// and breaks all blocks
// remember that game.js should put the players in actual positions given to them by the server
// not just random.

// dispatchEvent(new KeyboardEvent("keyup", {
//     key: Player.controls[dir]
//     , stopPropagation: true
// }));
class AI extends Player{
    constructor(ground){
        super(ground);
        this.moving = false;
        this.dirs = {x: 0, y: 0};
        this.movInterval = setInterval(()=>{
            this.moveRandom();
        }, 100);
    }

    moveCircular(){
        // turning algorithm
         
    }

    event(){}
    moveRandom(){
        // 'random' algorithm (chooses a random block and goes to break it)
        if (this.moving){
            // 2
            console.log(this.dirs);
            if (this.dirs.x && this.move(2-this.dirs.dx) != 2){ //-1: 3, 1: 1. left, right
                this.dirs.x -= this.dirs.dx;
            } else if (this.dirs.y && this.move(1+this.dirs.dy)){ //-1: 0, 1: 2. up, down
                this.dirs.y -= this.dirs.dy;
            } else{
                this.moving = false;
                clearInterval(this.movInterval);
            }
        } else{
            this.moving = true;
            let randomWood = choice(Block.blocks[1]).position;
            console.log(this.ground.position, randomWood);
            this.dirs.x = randomWood[0] - this.ground.position[0]; 
            this.dirs.y = randomWood[1] - this.ground.position[1];
            this.dirs.dx = Math.sign(this.dirs.x);
            this.dirs.dy = Math.sign(this.dirs.y);
        }
    }
}