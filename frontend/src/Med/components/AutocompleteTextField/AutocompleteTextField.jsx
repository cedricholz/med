// import React, { useEffect, useState } from "react"
// import { Autocomplete } from "@mui/material"
// import TextField from "@mui/material/TextField"
// import Axios from "../../../Util/Axios"
// const CancelToken = Axios.getCancelToken()
// let cancel
// const AutocompleteTextField = ({ autocompleteUrl, onSelect, defaultValue }) => {
//   const [loading, setLoading] = useState(false)
//   const [options, setOptions] = useState([])
//   const [searchValue, setSearchValue] = useState("")
//
//   useEffect(() => {}, [])
//
//   const getData = (searchValue) => {
//     Axios.get(`${autocompleteUrl}?search=${searchValue}`, {
//       cancelToken: new CancelToken(function executor(c) {
//         cancel = c
//       }),
//     })
//       .then(({ data }) => {
//         setOptions(
//           data.results.map((option) => {
//             return {
//               label: option.name,
//               value: option.id,
//             }
//           })
//         )
//       })
//       .catch((e) => {
//         if (Axios.isCancel(e)) {
//         } else {
//           setLoading(false)
//         }
//       })
//   }
//
//   return (
//     <Autocomplete
//       disablePortal
//       options={options}
//       defaultValue={defaultValue}
//       onChange={(event, value) => {
//         let option = value
//         onSelect(option)
//       }}
//       renderInput={(params) => (
//         <TextField
//           value={searchValue}
//           {...params}
//           onChange={(event) => {
//             setSearchValue(event.target.value)
//             getData(event.target.value)
//           }}
//         />
//       )}
//     />
//   )
// }
//
// export default AutocompleteTextField
