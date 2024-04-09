import React, { useEffect, useState } from "react"

// react-router components
// @mui material components
// import CookieConsent from "react-cookie-consent"
import AppRouter from "./AppRouter/AppRouter"
// import Cookies from "js-cookie"
import "@mantine/core/styles.css"
// react-router components
import { useLocation, useNavigate } from "react-router-dom"
// @mui material components
import { useDispatch } from "react-redux"
import Toast from "./Med/components/core/Toast/Toast"

const App = () => {
  // const consentCookieName = "med_consent_cookies"
  // const consentCookie = Cookies.get(consentCookieName)
  const [isAuthenticated, setIsAuthenticated] = useState(null)
  const { pathname } = useLocation()
  const mainDispatch = useDispatch()
  const navigate = useNavigate()
  useEffect(() => {
    console.log("SUP")
  }, [])
  useEffect(() => {
    if (process.env.REACT_APP_ENV === "production") {
      // ReactPixel.init("XXXX") // TODO
      // ReactGA.initialize([
      //     {
      //         trackingId: "XXXX", // TODO
      //     },
      // ])
      // ReactGA.ga("consent.revoke")
      // if (!consentCookie) {
      //     ReactGA.ga("consent.revoke")
      //     ReactPixel.revokeConsent()
      // }
    }
  }, [])

  // localStorage.removeItem("token")
  let token = localStorage.getItem("token")
  useEffect(() => {
    setIsAuthenticated(!!token)
  }, [token])

  return (
    <>
      {pathname.startsWith("/staff") && isAuthenticated && (
        <>
          <div>ayyy stafferoni</div>
        </>
      )}
      <Toast />
      <AppRouter />
      {/*  <CookieConsent*/}
      {/*      location="bottom"*/}
      {/*      buttonText="Accept"*/}
      {/*      cookieName={consentCookieName}*/}
      {/*      style={{*/}
      {/*          background: "#FFFFFF",*/}
      {/*          color: "#fff",*/}
      {/*          fontSize: "14px",*/}
      {/*          zIndex: 1201,*/}
      {/*      }}*/}
      {/*      buttonStyle={{*/}
      {/*          background: "#0073ce",*/}
      {/*          color: "white",*/}
      {/*          fontSize: "14px",*/}
      {/*          borderRadius: "2px",*/}
      {/*      }}*/}
      {/*      declineButtonStyle={{*/}
      {/*          background: "transparent",*/}
      {/*          borderRadius: "2px",*/}
      {/*          border: "none",*/}
      {/*          color: "black",*/}
      {/*          fontSize: "14px",*/}
      {/*      }}*/}
      {/*      expires={150}*/}
      {/*      enableDeclineButton*/}
      {/*      declineButtonText="Decline"*/}
      {/*      onAccept={() => {*/}
      {/*          ReactPixel.grantConsent()*/}
      {/*          ReactGA.ga("consent.grant")*/}
      {/*      }}*/}
      {/*      onDecline={() => {*/}
      {/*          // Handle the decline action here*/}
      {/*      }}*/}
      {/*  >*/}
      {/*      <div*/}
      {/*          style={{*/}
      {/*              color: "black",*/}
      {/*          }}*/}
      {/*      >*/}
      {/*          This website uses cookies to enhance your experience. By accepting,*/}
      {/*          you consent to the use of cookies.*/}
      {/*          <span style={{fontSize: "12px", marginLeft: "5px"}}>*/}
      {/*  <a href="/cookies" style={{color: "#0073ce"}}>*/}
      {/*    View Cookie Policy*/}
      {/*  </a>*/}
      {/*</span>*/}
      {/*      </div>*/}
      {/*  </CookieConsent>*/}
    </>
  )
}
export default App
