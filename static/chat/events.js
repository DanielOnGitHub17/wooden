import { Chat } from "./chat.js"

configureEvents({
    submit: [Chat.send]
    , load: [Chat.close]
    , keyup: [Chat.undo]
});
