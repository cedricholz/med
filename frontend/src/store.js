import { configureStore } from "@reduxjs/toolkit"
import cartReducer from "./slices/cartSlice"
import toastReducer from "./slices/toastSlice"

export const store = configureStore({
  reducer: {
    cart: cartReducer,
    toast: toastReducer,
  },
})
