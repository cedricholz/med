import React from "react"

import "./Hero.css"

import { Button, Container, Overlay, Text, Title } from "@mantine/core"

const Hero = () => {
  return (
    <div className={"hero"}>
      <Overlay
        gradient="linear-gradient(180deg, rgba(0, 0, 0, 0.25) 0%, rgba(0, 0, 0, .65) 40%)"
        opacity={1}
        zIndex={0}
      />
      <Container className={"heroContainer"} size="md">
        <div className={"heroTitle"}>Protocali: Medical Data Aggregator</div>

        <Text className={"heroDescription"} size="xl" mt="xl">
          Save time and money with Protocali. We provide a secure and easy way
          to get your data in the format you need right away.
        </Text>

        <Button
          variant="gradient"
          size="xl"
          radius="xl"
          className={"heroControl"}
        >
          Book a Demo
        </Button>
      </Container>
    </div>
  )
}

export default Hero
