import { configureStore } from '@reduxjs/toolkit'
import userReducer from './userSlice'
import chatReducer from './chatSlice'
import filesReducer from './filesSlice';


export const store = configureStore({
  reducer: {
    user: userReducer,
    chat: chatReducer,
    files: filesReducer,
  },
})