import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    chatSessions: [],
    currentChatId: -1
}

export const chatSlice = createSlice({
    name: 'chat',
    initialState,
    reducers: {
        setCurrentChatId: (state, action) => {
            state.currentChatId = action.payload
        },
        setChatSessions: (state, action) => {
            state.chatSessions = action.payload
        },
        setToken: (state, action) => {
            const chat_session_id = action.payload.chat_session_id;
            const ai_message_id = action.payload.ai_message_id;
            const token = action.payload.token;
            
            state.chatSessions[chat_session_id].messages[ai_message_id].text += token;
            console.log(state.chatSessions[chat_session_id])
        }
    },
})

// Action creators are generated for each case reducer function
export const { setChatSessions, setCurrentChatId, setToken } = chatSlice.actions

export default chatSlice.reducer
