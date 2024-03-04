class Bot extends Player{
    constructor(ground, name){
        super(ground, name);
        this.moving = false;
        this.dirs = [];
        this.movInterval = setInterval(()=>{
            this.moveRandom();
        }, 200);
        transfer(this, Player.players, Bot.bots);
        this.body.className += " bot";
    }

moveCircular(){
        // turning algorithm
         
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
            this.dirs[0] = 2*(this.randomWood[0]>=this.ground.position[0])
            // 1/3 for right/left
            this.dirs[1] =  1 + 2*(this.ground.position[1]>=this.randomWood[1]);
        }
    }
    static bots = [];
}

// // https://youtu.be/w4EdnxNjrhc
// // "Too much code. If else's or repetitions are more reasonable, I think. This is just... too much"
// for (let i=0; i<2; i++){
//     // !change ensures that left/right won't run if up/down has before.
//     // up/down will always run first until it is good enough
//     // !=. trust the process. // trust that it will not increase more than it is supposed to
//     // (>= means something else.)
//     // if you have doubts, you can use near from funcs.js.
//     if (!change && this.ground.position[i] != this.randomWood[i]){
//         this.move(this.dirs[i]);
//         change += 1;
//         // break (2/23/24) --> check later to see why
//     }
// }
// if (!change){
//     this.moving = false;
// }
// // for (let i=0; i<2; i++){
// //     // po
// //     // 0,2 for up/down. 3/1 for right/left
// //     this.dirs[i] = i + 2*(this.randomWood[i] - this.ground.position[i] >= 0);
// // }
// // this.dirs[1] = 4 - this.dirs[1]; // set things right (or left)
// // 1+-1=0(up):1+1(2)