import { username } from "../scripts.js";

class Chat {
    constructor(from, message, time /*"previous", "to" for later */) {
        Chat.chats.push(this);
        [this.from, this.message, this.time] = [from, message, time]
        this.build()
    }

    build() {
        // Remember to make reclass return the dom
        reclass(add(this.BOX = make(), CHATS), "chat");
        for (let prop in Chat.props) {
            add(this[prop.toUpperCase()] = make(Chat.props[prop]), this.BOX)
                .textContent = this[prop];
        }

        let time = new Date(this.TIME.dateTime = this.time);
        time.setSeconds(0);
        this.TIME.textContent = time.toLocaleTimeString().split(":00").join("");

        // Scroll
        this.BOX.scrollIntoViewIfNeeded();
    }

    static send(event) {
        // event from chatbox form
        if (event.target != CHATBOX) return;
        event.preventDefault();
        if (!INPUT.value.trim()) {
            let formerError = ERRORS.textContent;
            ERRORS.textContent = "Can't send an empty message";
            MESSAGES.className = "show";
            setTimeout(() => {
                // Attempt to restore former error message, multiple !INPUT.value.trim() will set formerError to 
                // "Can't send an empty message" again, so this might not work as expected.
                ERRORS.textContent = formerError;
                MESSAGES.className = "empty";
            }, 1000);
            return
        }

        // Put date in UTC. Clients can convert as needed. Clients won't know timezone of others.
        Chat.socket.send(jsonStr([username, INPUT.value, (new Date()).toISOString()]));
        INPUT.saved = INPUT.value  // do an undo feature,
        INPUT.value = "";
    }

    static undo(event) {
        // Undo feature - does undo only one step back
        if (!(event.target == INPUT && event.ctrlKey && event.key == "z")) return;
        event.preventDefault();
        INPUT.value = INPUT.saved || "";
    }

    static message(event) {
        if (event.target != Chat.socket) return;
        new Chat(...jsonObj(event.data));
    }

    static error(event) {
        event.preventDefault();
        if (event.target != Chat.socket) return;
        Chat.close();
    }

    // static 
    /*
    Write events here, no need for a chat socket, Chat.socket will handle
    The events will be static methods, add them to events.js
    like: "message": [Chat.message], "error": "", "whatnot"
    */

    static props = { "from": "span", "message": 'p', "time": "time" };
    static chats = [];
    static close() {
        Chat.socket = new WebSocket(`ws${(location.protocol == "https:") ? 's' : ''}://${location.host}/ws/chat/`);
        ["open", "close", "message", "error"].forEach(
            type => Chat.socket.addEventListener(type, Chat[type])
        );
    }
}

export { Chat }