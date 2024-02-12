// world.innerHTML = ''
class Game{
    constructor(){
        this.gameRawMaterial = [...Game.world.children].map(i=>JSON.parse(i.textContent))
        Game.world.innerHTML = '';
        this.length = this.gameRawMaterial.length;
        Game.world.style.width = this.length*Block.dimension + 'px';
        for (let i in this.gameRawMaterial){
            this.gameRawMaterial[i].forEach(kind => {
                new Block(kind);
            });
        }
    }

    start(){
        3
    }
    static world = get('world');
}
let game = new Game()