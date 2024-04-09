import React from "react"
import ReactDOM from "react-dom/client"
import "./index.css"
import App from "./App"
import reportWebVitals from "./reportWebVitals"
import { BrowserRouter } from "react-router-dom"

import { Provider } from "react-redux"
import { localStorageColorSchemeManager } from "@mantine/core"
import { store } from "./store"
import { createTheme, MantineProvider } from "@mantine/core"

const root = ReactDOM.createRoot(document.getElementById("root"))

const theme = createTheme({
  /** Put your mantine theme override here */
})

root.render(
  <BrowserRouter>
    <Provider store={store}>
      {/*<SoftUIControllerProvider>*/}
      <MantineProvider
        defaultColorScheme="auto"
        colorSchemeManager={localStorageColorSchemeManager({
          key: "mantine-ui-color-scheme",
        })}
        // theme={theme}
        // withGlobalStyles
        // withNormalizeCSS
      >
        <App />
      </MantineProvider>
      {/*</SoftUIControllerProvider>*/}
    </Provider>
  </BrowserRouter>
)

// If you want to start measuring performance in your app, pass a function
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
