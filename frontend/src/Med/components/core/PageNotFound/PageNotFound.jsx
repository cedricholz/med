import React, { useEffect } from "react"

const PageNotFound = () => {
  // const navigate = useNavigate()

  useEffect(() => {
    document.documentElement.scrollTop = 0
    document.scrollingElement.scrollTop = 0
  }, [])

  return <div>Page not found</div>
  // return (
  //   <Page>
  //     <Box
  //       sx={{
  //         display: "flex",
  //         minHeight: "100vh",
  //         backgroundColor: "#1d2f3e",
  //       }}
  //     >
  //       <Grid
  //         container
  //         direction="column"
  //         justifyContent="center"
  //         alignItems="center"
  //         background={primary}
  //       >
  //         <Typography variant="h1" style={{ color: "white" }}>
  //           404
  //         </Typography>
  //         <Typography variant="h6" style={{ color: "white" }}>
  //           Page does not exist
  //         </Typography>
  //       </Grid>
  //     </Box>
  //   </Page>
  // )
}

export default PageNotFound
