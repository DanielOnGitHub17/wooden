// world.innerHTML = ''
class Game{
    constructor(){
        this.world = get('world');
        this.gameRawMaterial = [...world.children].map(i=>JSON.parse(i.textContent))
        this.world.innerHTML = '';
        this.backgrounds = ["blank", "wood", "iron"];
        for (let i in this.gameRawMaterial){
            this.gameRawMaterial[i].forEach(element => {
                4
            });
        }
    }

    start(){
        3
    }
}
let game = new Game()