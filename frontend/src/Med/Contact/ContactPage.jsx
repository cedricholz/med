import React from "react"
import Page from "../Page/Page"
import { Box, Typography } from "@mui/material"
import Contact from "./Contact"

const ContactPage = () => {
  let textShadow = "3px 3px 4px #000000"

  return (
    <Page>
      <Box
        sx={{
          backgroundColor: "#1d2f3e",
          color: "white",
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          // justifyContent: "center",
          textAlign: "center",
          // px: [2, 4],
          pt: 5,
        }}
      >
        <Typography variant="h2" sx={{ marginBottom: 2, textShadow }}>
          Contact
        </Typography>
        <Box
          sx={{
            py: 5,
            px: [2, 4],
            width: "100%",
            maxWidth: 500,
          }}
        >
          {/*<Typography*/}
          {/*  variant="h5"*/}
          {/*  sx={{ marginBottom: 3, fontFamily: "Josefin Sans" }}*/}
          {/*>*/}
          {/*  If you need a custom board, want to stock Marlin Boards in your shop*/}
          {/*  or just want to say hey, send me a message down below.*/}
          {/*</Typography>*/}
        </Box>
        <Box
          sx={{
            maxWidth: 700,
          }}
          pb={10}
        >
          <Contact p={2} />
        </Box>
      </Box>
    </Page>
  )
}

export default ContactPage
