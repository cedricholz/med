import React, { lazy, useRef, useState } from "react"
import { Box, Button, Chip } from "@mui/material"
import TextField from "@mui/material/TextField"
import Axios from "../../Util/Axios"
import { updateToastData } from "../../slices/toastSlice"

import { useDispatch } from "react-redux"
import IconButton from "@mui/material/IconButton"
import ImageIcon from "@mui/icons-material/Image"
import ClearIcon from "@mui/icons-material/Clear"
import { uploadFileToAws } from "../../Util/Aws"
import "./contact.css"

const Zoom = lazy(() => import("react-medium-image-zoom")) // Necessary for sitemap

const Contact = ({
  starterMessage,
  p,
  ml,
  mr,
  backgroundColor = "#f5f5f5",
  onSuccess = () => {},
}) => {
  const [loading, setLoading] = useState(false)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [message, setMessage] = useState(starterMessage)
  const [messageSent, setMessageSent] = useState(false)
  const dispatch = useDispatch()
  const fileUploadRef = useRef(null)
  const [files, setFiles] = useState([])

  return (
    <Box ml={ml} mr={mr}>
      <Box
        sx={{
          backgroundColor: backgroundColor,
          borderRadius: 2,
          width: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {messageSent && (
          <Box pt={5}>
            {/*<Typography*/}
            {/*  sx={{*/}
            {/*    color: darkBlue,*/}
            {/*    fontFamily: "Josefin Sans",*/}
            {/*    fontWeight: "Bold",*/}
            {/*    fontSize: "1.2rem",*/}
            {/*  }}*/}
            {/*>*/}
            {/*  Message Sent Successfully*/}
            {/*</Typography>*/}

            <Chip
              label="Message Sent Successfully"
              sx={{
                fontSize: "1.2rem",
              }}
              color={"secondary"}
            />
          </Box>
        )}
        <Box p={p}>
          <TextField
            disabled={loading}
            margin="normal"
            required
            fullWidth
            label={"Name"}
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
          <TextField
            disabled={loading}
            margin="normal"
            required
            fullWidth
            label={"Email"}
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />

          <TextField
            disabled={loading}
            margin="normal"
            fullWidth
            label={"Phone"}
            value={phone}
            onChange={(event) => setPhone(event.target.value)}
          />

          <Box
            mt={1}
            sx={{
              display: "flex",
              justifyContent: "flex-end",
            }}
          >
            <IconButton
              color="primary"
              onClick={() => {
                fileUploadRef.current.click()
              }}
            >
              <ImageIcon />
            </IconButton>
          </Box>

          <TextField
            disabled={loading}
            margin="normal"
            required
            fullWidth
            multiline
            rows={6}
            label={"Message"}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
          />
          <Box mt={2}>
            <div className="file-previews">
              {files.map((fileObj, i) => (
                <div key={i} className="file-preview">
                  <Zoom>
                    <img src={fileObj.url} alt="File preview" />
                  </Zoom>

                  <IconButton
                    component={Button}
                    style={{
                      color: "#fc3158",
                    }}
                    onClick={() => {
                      // Remove the file from the array
                      let newFiles = files.filter((_, index) => index !== i)
                      setFiles(newFiles)
                    }}
                  >
                    <ClearIcon />
                  </IconButton>
                </div>
              ))}
            </div>
          </Box>
          <Button
            variant="contained"
            color="primary"
            disabled={loading || !email || !name}
            sx={{ mt: 3, width: "100%", textTransform: "none" }}
            onClick={() => {
              setLoading(true)
              Axios.post("/api/site-configuration/action_contact/", {
                email: email,
                name: name,
                message: message,
                phone: phone,
                files: files,
              })
                .then((resp) => {
                  setLoading(false)
                  setName("")
                  setEmail("")
                  setPhone("")
                  setMessage("")
                  setFiles([])
                  setMessageSent(true)

                  dispatch(
                    updateToastData({
                      message: "Message sent successfully",
                      severity: TOAST_SEVERITY_SUCCESS,
                    })
                  )
                  onSuccess()
                })
                .catch((e) => {
                  setLoading(false)
                  dispatch(
                    updateToastData({
                      message: "Error sending message",
                      severity: TOAST_SEVERITY_ERROR,
                    })
                  )
                })
            }}
          >
            Submit
          </Button>
        </Box>
      </Box>
      <input
        style={{ display: "none" }}
        ref={fileUploadRef}
        type="file"
        multiple
        onChange={(event) => {
          const newFiles = Array.from(event.target.files)
          let promises = []
          for (let file of newFiles) {
            promises.push(uploadFileToAws(file))
          }
          Axios.all(promises)
            .then((resps) => {
              setFiles([...files, ...resps])
            })
            .catch((e) => {
              dispatch(
                updateToastData({
                  message: e,
                  severity: TOAST_SEVERITY_ERROR,
                })
              )
            })
        }}
      />
    </Box>
  )
}

export default Contact
