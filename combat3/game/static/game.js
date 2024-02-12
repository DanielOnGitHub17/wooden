const GAMERAWMATERIAL = [...world.children].map(i=>JSON.parse(i.textContent))
// world.innerHTML = ''
class Game{
    constructor(){
        this.world = get('world');
        this.backgrounds = ["blank", "wood", "iron"]
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