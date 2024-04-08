import React, { useEffect, useState } from "react"

import { Navigate, Route, Routes } from "react-router-dom"
import Home from "../Med/Home/Home"
import PageNotFound from "../Med/components/core/PageNotFound/PageNotFound"

const ProtectedRoute = ({ children, isAuthenticated }) => {
  if (isAuthenticated === false) {
    return <Navigate to="/signin" replace />
  }
  // return <ThemeProvider theme={staffTheme}> {children} </ThemeProvider>
  return <>{children}</>
}
const UserRoute = ({ children }) => {
  // return <ThemeProvider theme={userTheme}> {children} </ThemeProvider>
  return <>{children}</>
}
const StaffUserRoute = ({ children, isAuthenticated }) => {
  if (isAuthenticated === false) {
    return <Navigate to="/signin" replace />
  }
  return <>{children}</>
  // return <ThemeProvider theme={userTheme}> {children} </ThemeProvider>
}

const AppRouter = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(null)

  useEffect(() => {
    setIsAuthenticated(!!localStorage.getItem("token"))
  }, [])

  return (
    <Routes>
      {/*<Route*/}
      {/*  path="/signin"*/}
      {/*  element={*/}
      {/*    <SignInPage*/}
      {/*      isAuthenticated={isAuthenticated}*/}
      {/*      setIsAuthenticated={setIsAuthenticated}*/}
      {/*    />*/}
      {/*  }*/}
      {/*  key="signin"*/}
      {/*/>*/}
      {/*<Route*/}
      {/*  exact*/}
      {/*  path={"/staff"}*/}
      {/*  element={*/}
      {/*    <ProtectedRoute isAuthenticated={isAuthenticated}>*/}
      {/*      <StaffComponent>*/}
      {/*        <Dashboard />*/}
      {/*      </StaffComponent>*/}
      {/*    </ProtectedRoute>*/}
      {/*  }*/}
      {/*/>*/}
      {/*<Route*/}
      {/*  exact*/}
      {/*  path={"/custom-surfboard-order-staff-preset"}*/}
      {/*  element={*/}
      {/*    <StaffUserRoute>*/}
      {/*      <CustomOrder isStaff={true} presetEditor={true} />*/}
      {/*    </StaffUserRoute>*/}
      {/*  }*/}
      {/*/>*/}
      {/*<Route*/}
      {/*  exact*/}
      {/*  path={"/contact"}*/}
      {/*  element={*/}
      {/*    <UserRoute>*/}
      {/*      <ContactPage />*/}
      {/*    </UserRoute>*/}
      {/*  }*/}
      {/*/>*/}
      <Route
        exact
        path={"/"}
        element={
          <UserRoute>
            <Home />
          </UserRoute>
        }
      />
      <Route
        exact
        path={"*"}
        element={
          <UserRoute>
            <PageNotFound />
          </UserRoute>
        }
      />
    </Routes>
  )
}

export default AppRouter
