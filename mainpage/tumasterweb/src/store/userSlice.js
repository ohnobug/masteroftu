import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  userinfo: null
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUserinfo: (state, action) => {
      state.userinfo = action.payload
    },
  },
})

// Action creators are generated for each case reducer function
export const { setUserinfo } = userSlice.actions

export default userSlice.reducer
