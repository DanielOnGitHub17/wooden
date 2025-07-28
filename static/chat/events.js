import { makeEvents } from "../scripts.js"
import { Chat } from "./chat.js"

makeEvents({
    submit: [Chat.send]
    , load: [Chat.close]
    , keyup: [Chat.undo]
});
