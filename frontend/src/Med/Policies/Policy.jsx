import React, { useEffect } from "react"
import { createTheme, ThemeProvider } from "@mui/material/styles"
import NavBar from "../NavBar/NavBar"
import { Typography } from "@mui/material"
import Container from "@mui/material/Container"
import Box from "@mui/material/Box"
import Footer from "../../components/core/Footer/Footer"
import Page from "../Page/Page"

const Policy = ({ children, name }) => {
  useEffect(() => {}, [])
  const policyTheme = createTheme({
    components: {
      MuiTypography: {
        styleOverrides: {
          root: {
            fontFamily: "Josefin Sans",
          },
        },
      },
    },
  })
  return (
    <Page>
      <ThemeProvider theme={policyTheme}>
        <Box sx={{ minHeight: "100vh" }}>
          <Box mt={5}>
            <Container>
              <Typography variant="h2" align="left" gutterBottom>
                {name}
              </Typography>
              <Box my={2} mt={7} textAlign="left">
                {children}
              </Box>
            </Container>
          </Box>
        </Box>
      </ThemeProvider>
    </Page>
  )
}

export default Policy
