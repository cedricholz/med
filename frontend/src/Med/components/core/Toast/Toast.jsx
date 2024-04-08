import React from "react"
// import { Alert, Snackbar } from "@mui/material"
import { useDispatch, useSelector } from "react-redux"
import { updateToastData } from "../../../../slices/toastSlice"

export const TOAST_SEVERITY_ERROR = "error"
export const TOAST_SEVERITY_WARNING = "warning"
export const TOAST_SEVERITY_INFO = "info"
export const TOAST_SEVERITY_SUCCESS = "success"

const Toast = ({ action }) => {
  const dispatch = useDispatch()
  const { toast } = useSelector((state) => state)
  const toastData = toast.toastData
  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return
    }
    dispatch(updateToastData(null))
  }
  return <div></div>
  // return (
  //   <Snackbar
  //     open={!!toastData}
  //     autoHideDuration={toastData?.duration || 3000}
  //     onClose={handleClose}
  //     action={action}
  //   >
  //     <Alert
  //       onClose={handleClose}
  //       severity={toastData?.severity}
  //       sx={{ width: "100%" }}
  //     >
  //       {toastData?.message}
  //     </Alert>
  //   </Snackbar>
  // )
}

export default Toast
