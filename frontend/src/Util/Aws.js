import Axios from "./Axios"
import axios from "axios"
const s3Axios = axios.create()
export const uploadFileToAws = (file) => {
  return Axios.post("/api/site-configuration/get_aws_put_url/", {
    file_name: file.name,
    content_type: file.type,
  })
    .then(({ data }) => {
      const { url, put_url } = data

      let headers = {
        "x-amz-storage-class": "INTELLIGENT_TIERING",
        "content-type": file.type,
      }
      return s3Axios
        .put(put_url, file, {
          headers: headers,
        })
        .then((resp) => {
          return new Promise((resolve) => {
            resolve({ url })
          })
        })
        .catch((e) => {
          console.log("Axios Error", e)
          return new Promise((resolve, reject) => {
            reject(e)
          })
        })
    })
    .catch((e) => {
      return new Promise((resolve, reject) => {
        reject(null)
      })
    })
}
