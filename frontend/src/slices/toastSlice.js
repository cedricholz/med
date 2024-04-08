import { createSlice } from "@reduxjs/toolkit"

const initialState = {
  toastData: null,
}

export const toastSlice = createSlice({
  name: "toast",
  initialState,
  reducers: {
    updateToastData: (state, action) => {
      if (action.payload) {
        action.payload.message = (action.payload.message || "").toString()
      }
      state.toastData = action.payload
    },
  },
})

export const { updateToastData } = toastSlice.actions

export default toastSlice.reducer
