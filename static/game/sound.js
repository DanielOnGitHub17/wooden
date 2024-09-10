class Sound {
    static stopAll() {
        for (let sound of Object.values(Sound.sounds)) {
            sound.pause();
        }
    }

    static play(name) {
        return Sound.sounds[name].play();
    }

    static stop(name) {
        Sound.sounds[name].pause();
    }

    static loop(name) {
        Sound.sounds[name].loop = true;
        Sound.sounds[name].play();
    }

    static loadSounds(sources = Sound.sources) {
        let sounds = {};
        for (let name of sources) {
            sounds[name.split('.')[0]] = new Audio(`/static/game/sound/${name}`);
        };
        return sounds;
    }

    static load() {
        Sound.sounds = Sound.loadSounds();
        Sound.loaded = true;
    }

    static sources = ["game_music.wav", "lounge_music.mp3", "pile_player.mp3", "player_move.wav", "stopped_hitting.mp3", "waiting_music.wav", "wood_break.wav", "wood_hit.wav"];
    static sounds = {};
}

export { Sound }
