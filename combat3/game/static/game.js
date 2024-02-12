// world.innerHTML = ''
class Game{
    constructor(){
        this.world = get('world');
        this.gameRawMaterial = [...world.children].map(i=>JSON.parse(i.textContent))
        this.world.innerHTML = '';
        this.backgrounds = ["blank", "wood", "iron"];
        for (let i in GAMERAWMATERIAL){
            GAMERAWMATERIAL[i].forEach(element => {
                4
            });
        }
    }

    start(){
        3
    }
}