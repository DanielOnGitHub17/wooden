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
        this.dirs = [];
        this.movInterval = setInterval(()=>{
            this.moveRandom();
        }, 200);
    }

    moveCircular(){
        // turning algorithm
         
    }

    event(){}
    moveRandom(){
        // 'random' algorithm (chooses a random block and goes to break it)
        if (this.moving){
            let  change = 0;
            for (let i=0; i<2; i++){
                // !change ensures that left/right won't run if up/down has before.
                // up/down will always run first until it is good enough
                // !=. trust the process. // trust that it will not increase more than it is supposed to
                // if you have doubts, you can use near from funcs.js.
                if (!change && this.ground.position[i] != this.randomWood[i]){
                    this.move(this.dirs[i]);
                    change += 1;
                }
            }
            if (!change){
                this.moving = false;
                clearInterval(this.movInterval);
            }
        } else{
            this.moving = true;
            let randomWood = choice(Block.blocks[1]).position;
            for (let i=0; i<2; i++){
                // 0,2 for up/down. 3/1 for right/left
                this.dirs[i] = i + 2*(randomWood[i] - this.ground.position[i] >= 0);
            }
            this.dirs[1] = 4 - this.dirs[1]; // set things right (or left)
            console.log(this.ground.position, randomWood, this.dirs);
            this.randomWood = randomWood;
            // 1+-1=0(up):1+1(2)
        }
    }
}

// style blocks according to number of breaks friendly blocks to hard ones
// blocks change on hit to other type
// wood.strength
addEventListener("keyup", (event)=>{event.key=='p' && clearInterval(1)})