import React from "react"
import NavBar from "../NavBar/NavBar"
import Footer from "../../components/core/Footer/Footer"
import Link from "@mui/material/Link"
import { Box, Breadcrumbs, Grid, Typography } from "@mui/material"

const Page = ({ children, backgroundColor }) => {
  return (
    <React.Fragment>
      <NavBar position={"relative"} />
      <div
        style={{
          minHeight: "100vh",
          backgroundColor: backgroundColor,
          marginTop: "54px",
        }}
      >
        {children}
      </div>
      <Footer />
    </React.Fragment>
  )
}

export default Page
