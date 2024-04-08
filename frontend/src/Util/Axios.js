import axios from "axios"

axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFToken"

let navigateFunc
const setDefaults = (navigate) => {
  const token = localStorage.getItem("token")
  // if (process.env.NODE_ENV !== "development") {
  // axios.defaults.baseURL = "http://localhost:8000"
  //   axios.defaults.baseURL = "https://marlin.surf"
  // axios.defaults.baseURL = "https://staging.marlin.surf"
  // }
  if (window.location.pathname.includes("staff")) {
    axios.defaults.withCredentials = true
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`
  }

  navigateFunc = navigate
}

export default class Axios extends axios {
  static getModifiedConfig = (config, data) => {
    return config
  }

  static getCancelToken = () => {
    return axios.CancelToken
  }

  static isCancel = (e) => {
    return axios.isCancel(e)
  }

  static all = (requests, navigate) => {
    setDefaults(navigate)
    return Promise.all(requests)
      .then((resps) => {
        return new Promise((resolve) => {
          resolve(resps)
        })
      })
      .catch((e) => {
        return new Promise((resolve, reject) => {
          reject(e)
        })
      })
  }

  static get = (url, navigate, config) => {
    setDefaults(navigate)
    return axios
      .get(url, config)
      .then((resp) => {
        return new Promise((resolve) => {
          resolve(resp)
        })
      })
      .catch((e) => {
        return new Promise((resolve, reject) => {
          reject(e)
        })
      })
  }

  static post = (url, data, navigate, config) => {
    setDefaults(navigate)
    return axios
      .post(url, data, Axios.getModifiedConfig(config, data))
      .then((resp) => {
        return new Promise((resolve, reject) => {
          resolve(resp)
        })
      })
      .catch((e) => {
        return new Promise((resolve, reject) => {
          reject(e)
        })
      })
  }

  static patch = (url, data, navigate, config) => {
    setDefaults(navigate)
    return axios
      .patch(url, data, Axios.getModifiedConfig(config, data))
      .then((resp) => {
        return new Promise((resolve, reject) => {
          resolve(resp)
        })
      })
      .catch((e) => {
        return new Promise((resolve, reject) => {
          reject(e)
        })
      })
  }
  static put = (url, data, navigate, config) => {
    setDefaults(navigate)
    return axios
      .put(url, data, Axios.getModifiedConfig(config, data))
      .then((resp) => {
        return new Promise((resolve, reject) => {
          resolve(resp)
        })
      })
      .catch((e) => {
        return new Promise((resolve, reject) => {
          reject(e)
        })
      })
  }

  static delete = (url, navigate, config) => {
    setDefaults(navigate)
    return axios
      .delete(url, config)
      .then((resp) => {
        return new Promise((resolve, reject) => {
          resolve(resp)
        })
      })
      .catch((e) => {
        return new Promise((resolve, reject) => {
          reject(e)
        })
      })
  }
}

axios.interceptors.response.use(
  function (response) {
    return response
  },
  function (error) {
    const originalRequest = error.config

    if (!navigateFunc) {
      return Promise.reject(error)
    }

    if (
      error?.response?.status === 401 &&
      // error.response.data.detail === "Token is blacklisted" &&
      window.location.pathname.includes("staff") &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true
      localStorage.removeItem("token") // Remove the invalid token
      navigateFunc("/signin") // Redirect to the signin page
      return Promise.reject(error)
    }
    if (
      error?.response?.status === 401 &&
      !originalRequest._retry &&
      window.location.pathname.includes("staff")
    ) {
      originalRequest._retry = true
      return axios
        .post("/api/token/refresh/", {})
        .then((response) => {
          const newAccessToken = response.data.access
          localStorage.setItem("token", newAccessToken)
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${newAccessToken}`
          originalRequest.headers["Authorization"] = "Bearer " + newAccessToken
          return axios(originalRequest)
        })
        .catch((error) => {
          localStorage.removeItem("token") // Remove the invalid token
          navigateFunc("/signin") // Redirect to the signin page
          return Promise.reject(error)
        })
    }
    return Promise.reject(error)
  }
)
