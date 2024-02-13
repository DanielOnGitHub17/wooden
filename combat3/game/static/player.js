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
        let next = this.ground.position;
        next[0] += moves[dir][0];
        next[1] += moves[dir][1];
        let potentialGround = game.blocks.get(...next);
        if (!potentialGround){
            this.ground = potentialGround;
            this.ground.append(this.body);
        }
    }
    static moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
}