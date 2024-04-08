import React from "react"

const StaffRouteComponent = ({ children }) => {
  if (!localStorage.getItem("token")) {
    return <React.Fragment />
  }

  return <React.Fragment>{children}</React.Fragment>
}

export default StaffRouteComponent
