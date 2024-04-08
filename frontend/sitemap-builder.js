require("@babel/register")({
  presets: ["@babel/preset-env", "@babel/preset-react"],
})
require("ignore-styles")
const axios = require("axios")
global.window = {}
const router = require("./routes").default
const Sitemap = require("react-router-sitemap").default
const { JSDOM } = require("jsdom")
const apiUrl = "https://marlin.surf/"

async function generateSitemap() {
  const inventoryResponse = await axios.get(
    `${apiUrl}api/product-list/?type=inventory`
  )
  let inventoryIds = inventoryResponse.data.results.map((x) => x.id)

  const apparelResponse = await axios.get(
    `${apiUrl}api/product-list/?type=apparel`
  )
  let apparelIds = apparelResponse.data.results.map((x) => x.id)

  // let apparelIds = await fetchIds("apparel")

  const paramsConfig = {
    "/surfboard-inventory/:id": inventoryIds.map((id) => ({
      id,
    })),
    "/merchandise/:id": apparelIds.map((id) => ({
      id,
    })),
  }

  return new Sitemap(router)
    .applyParams(paramsConfig)
    .build("https://marlin.surf")
    .save("./public/sitemap.xml")
}

generateSitemap()
