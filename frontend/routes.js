// routes.js

import React from "react"
import InventoryPage from "./src/Med/Inventory/InventoryPage"
import { Route } from "react-router"

import Gallery from "./src/Med/Gallery/Gallery"
import About from "./src/Med/About/About"
import Faq from "./src/Med/Faq/Faq"
import Home from "./src/Med/Home/Home"
import CustomOrder from "./src/Med/CustomOrder/CustomOrder"
import CookiePolicy from "./src/Med/Policies/CookiePolicy"
import CartPage from "./src/Med/Cart/CartPage"
import ApparelList from "./src/Med/Apparel/ApparelList"
import ApparelPage from "./src/Med/Apparel/ApparelPage"
import PrivacyPolicy from "./src/Med/Policies/PrivacyPolicy"
import ContactPage from "./src/Med/Contact/ContactPage"
import InventoryList from "./src/Med/Inventory/InventoryList"

export default (
  <Route>
    <Route path="/" component={Home} />
    <Route path="/gallery" component={Gallery} />
    <Route path="/about" component={About} />
    <Route path="/faq" component={Faq} />

    <Route path="/merchandise/:id" component={ApparelPage} />
    <Route path="/merchandise" component={ApparelList} />
    <Route path="/surfboard-inventory/:id" component={InventoryPage} />
    <Route path="/surfboard-inventory" component={InventoryList} />

    <Route path="/cart" component={CartPage} />
    <Route path="/privacy" component={PrivacyPolicy} />
    <Route path="/cookies" component={CookiePolicy} />
    <Route path="/contact" component={ContactPage} />
    <Route path="/custom-surfboard-order/" component={Home} />
  </Route>
)
