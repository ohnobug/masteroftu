import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    chatSessions: {},
    currentChatId: -1
}

export const chatSlice = createSlice({
    name: 'chat',
    initialState,
    reducers: {
        // 设置当前退货
        setCurrentChatId: (state, action) => {
            state.currentChatId = action.payload
        },
        // 设置会话
        setChatSessions: (state, action) => {
            state.chatSessions = action.payload
        },
        // 设置消息
        setChatMessage: (state, action) => {
            const chat_session_id = action.payload.chat_session_id;
            const messages = action.payload.messages;
            state.chatSessions[chat_session_id].messages = messages;
        },
        // 设置token到消息
        setTokenToMessage: (state, action) => {
            const chat_session_id = action.payload.chat_session_id;
            const ai_message_id = action.payload.ai_message_id;
            const token = action.payload.token;
            state.chatSessions[chat_session_id].messages[ai_message_id].text += token;
        }
    },
})

// Action creators are generated for each case reducer function
export const { setChatSessions, setCurrentChatId, setTokenToMessage, setChatMessage } = chatSlice.actions

export default chatSlice.reducer
