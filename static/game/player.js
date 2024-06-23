class Player{
    constructor(ground, name){
        Player.players.push(this);
        this.name = name || "You";  // name will be 0 if playing with bots...
        this.ground = ground;
        this.hits = 0;
        this.blocksBroken = 0;
        this.next = ground.position;
        this.build();
        game.isMultiPlayer || this.event();
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
        this.body.style.rotate = `${dir*90}deg`;
        // moves by navigating through blocks
        // given the direction. it adds
        let [potentialGround, next] = this.nextGround(dir);
        if (potentialGround.kind != 1){
            this.hits = 0; // it turned away from a wood block.
            if (!potentialGround.kind){ // sand (change position)
                this.ground = potentialGround;
                add(this.body, this.ground.block);
                // if (this.name == Game.player) this.pos = this.ground.position;
                // time to learn about websockets in JS
                // and, apparently, Django channels
            }
        } else {// wood
            // if it hits the block game.hitsToBreak times, the block breaks
            if (JSON.stringify(this.next) == JSON.stringify(next)){ // checks if it's still hitting the same wooden block
                this.hits += 1;
                if (this.hits >= game.hits){ // the > is unneccesary
                    this.hits = 0;
                    potentialGround.crack();
                    this.blocksBroken += 1;
                    // if (this.name == Game.player) this.score = this.blocksBroken;
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
        window.addEventListener("keydown", (event)=>(Player.controls.includes(event.key) && event.preventDefault()));
        window.addEventListener("keyup", (event)=>{
            if (Player.controls.includes(event.key)){
                event.preventDefault();
                this.move(Player.controls.indexOf(event.key));
                // this.body.scrollIntoView();
            }
        })
    }

    data(){
        // return [] every useful thing of this player
    }

    send(){
        // send this.data() to server
    }

    set pos(value){
        let [r, c] = value;
        fetch(`/game/pos?r=${r}&c=${c}`).catch(error=>{});
    }

    set score(value){
        fetch(`/game/score?score=${value}`).catch(error=>{});
    }

    remove(){}

    static moves = [[-1, 0], [0, 1], [1, 0], [0, -1]];
    static controls = ["ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft"];
    static players = [];
}
