import React, { useState } from "react"
import { Navigate } from "react-router-dom"
import axios from "axios"

import Avatar from "@mui/material/Avatar"
import Button from "@mui/material/Button"
import CssBaseline from "@mui/material/CssBaseline"
import TextField from "@mui/material/TextField"
import Box from "@mui/material/Box"
import LockOutlinedIcon from "@mui/icons-material/LockOutlined"
import Typography from "@mui/material/Typography"
import Container from "@mui/material/Container"
import { createTheme, ThemeProvider } from "@mui/material/styles"
import Footer from "../components/core/Footer/Footer"
import { TOAST_SEVERITY_ERROR } from "../components/core/Toast/Toast"
import { useDispatch } from "react-redux"
import { updateToastData } from "../slices/toastSlice"
import Cookies from "js-cookie"

const SignInPage = ({ isAuthenticated, setIsAuthenticated }) => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [failed, setFailed] = useState(false)
  const [loading, setLoading] = useState(false)
  const dispatch = useDispatch()
  if (localStorage.getItem("token")) {
    return <Navigate to={"/staff"} />
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    Cookies.remove("refresh")
    let data = { username: username, password: password }
    axios
      .post("/api/token/", data)
      .then(async ({ data }) => {
        const { access, refresh } = data
        // Cookies.add("refresh", refresh)
        // await localStorage.setItem("refresh", refresh)
        localStorage.setItem("token", access)

        setLoading(false)

        // navigate("/dashboard")
        setIsAuthenticated(true)
      })
      .catch((e) => {
        Cookies.remove("refresh")
        localStorage.removeItem("token")
        dispatch(
          updateToastData({
            message: e,
            severity: TOAST_SEVERITY_ERROR,
          })
        )
        setLoading(false)
        setFailed(true)
      })
  }
  const defaultTheme = createTheme()
  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              disabled={loading}
              error={failed}
              onChange={(event) => {
                setUsername(event.target.value)
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              disabled={loading}
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              error={failed}
              onChange={(event) => {
                setPassword(event.target.value)
              }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              Sign In
            </Button>
          </Box>
        </Box>
        <Footer />
      </Container>
    </ThemeProvider>
  )
}

export default SignInPage
