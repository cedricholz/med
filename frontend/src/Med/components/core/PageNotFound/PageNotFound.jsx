import React, { useEffect } from "react"
import "./PageNotFound.css"
import { Illustration } from "./404Illustration"
import { Button, Container, Group, Title, Text } from "@mantine/core"
const PageNotFound = () => {
  return (
    <Container className={"pnfRoot"}>
      <div className={"pnfInner"}>
        <Illustration className={"pnfImage"} />
        <div className={"pnfContent"}>
          <Title>
            <div className="pnfTitle">Nothing to see here</div>
          </Title>
          <Text c="dimmed" size="lg" ta="center">
            <div className={"pnfDescription"}>
              Page you are trying to open does not exist. You may have mistyped
              the address, or the page has been moved to another URL. If you
              think this is an error contact support.
            </div>
          </Text>
          <Group justify="center">
            <Button
              size="md"
              onClick={() => {
                window.open("/", "_self")
              }}
            >
              Take me back to home page
            </Button>
          </Group>
        </div>
      </div>
    </Container>
  )
}

export default PageNotFound
