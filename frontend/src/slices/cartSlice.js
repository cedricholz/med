import { createSlice } from "@reduxjs/toolkit"

const initialState = {
  cart_items: [],
  cart_loaded: false,
}

export const cartSlice = createSlice({
  name: "cart",
  initialState,
  reducers: {
    updateCartItemsAction: (state, action) => {
      state.cart_items = action.payload
    },
    addToCartAction: (state, action) => {
      state.cart_items.push(action.payload)
    },
    removeFromCartAction: (state, action) => {
      state.cart_items = state.cart_items.filter((cartItem) => {
        return cartItem.id.toString() !== action.payload.toString()
      })
    },
    updateCartLoaded: (state, action) => {
      state.cart_loaded = true
    },
    updateCartItemQuantity: (state, action) => {
      let cart_item_id = action.payload.cart_item_id
      let cart_items = state.cart_items.map((cartItem) => {
        if (cartItem.id === cart_item_id) {
          cartItem.quantity = action.payload.quantity
        }
        return cartItem
      })
      state.cart_items = cart_items
    },
  },
})

export const {
  updateCartItemQuantity,
  removeFromCartAction,
  updateCartItemsAction,
  addToCartAction,
  updateCartLoaded,
} = cartSlice.actions

export default cartSlice.reducer
