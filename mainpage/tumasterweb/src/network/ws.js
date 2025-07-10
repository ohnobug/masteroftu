import { io } from "socket.io-client";
import { store } from "../store";
import { setToken } from "../store/chatSlice"

const socket = io(import.meta.env.VITE_WS_BASE_URL, {
    reconnectionDelayMax: 10000,
    extraHeaders: {
        authorization: `bearer aaaaaaaaaaaaaa`
    },
});

socket.on("connect", () => {
    console.log("链接成功")
});

socket.on("disconnect", () => {
    console.log("链接断开")
});


socket.on('token_output', (data) => {
    const jdata = JSON.parse(data);
    store.dispatch(setToken({
        chat_session_id: jdata.chat_session_id,
        ai_message_id: jdata.ai_message_id,
        token: jdata.token
    }))
});

export default socket;
