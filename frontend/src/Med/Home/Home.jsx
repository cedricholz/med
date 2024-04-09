import React from "react"
import Hero from "./Hero/Hero"
import FeaturesCards from "./FeaturesCards/FeaturesCards"
import Stats from "./Stats/Stats"
import Contact from "./Contact/Contact"
import Footer from "./Footer/Footer"

const Home = () => {
  return (
    <React.Fragment>
      <Hero />
      {/*<Features />*/}
      <Stats />
      <FeaturesCards />
      <Contact />
      <Footer />
    </React.Fragment>
  )
}

export default Home
