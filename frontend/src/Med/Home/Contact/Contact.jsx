import React from "react"

import {
  TextInput,
  Textarea,
  SimpleGrid,
  Group,
  Title,
  Button,
} from "@mantine/core"
import { useForm } from "@mantine/form"

const Contact = () => {
  //       setLoading(true)
  //   Axios.post("/api/site-configuration/action_contact/", {
  //     email: email,
  //     name: name,
  //     message: message,
  //     phone: phone,
  //     files: files,
  //   })
  //     .then((resp) => {
  //       setLoading(false)
  //       setName("")
  //       setEmail("")
  //       setPhone("")
  //       setMessage("")
  //       setFiles([])
  //       setMessageSent(true)
  //
  //       dispatch(
  //         updateToastData({
  //           message: "Message sent successfully",
  //           severity: TOAST_SEVERITY_SUCCESS,
  //         })
  //       )
  //       onSuccess()
  //     })
  //     .catch((e) => {
  //       setLoading(false)
  //       dispatch(
  //         updateToastData({
  //           message: "Error sending message",
  //           severity: TOAST_SEVERITY_ERROR,
  //         })
  //       )
  //     })
  // }}
  const form = useForm({
    initialValues: {
      name: "",
      email: "",
      subject: "",
      message: "",
    },
    validate: {
      name: (value) =>
        value.trim().length < 2 ? "Name must be at least 2 characters" : null,
      email: (value) => (!/^\S+@\S+$/.test(value) ? "Invalid email" : null),
      subject: (value) =>
        value.trim().length === 0 ? "Subject cannot be empty" : null,
    },
  })

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        paddingTop: 40,
      }}
    >
      <div style={{ maxWidth: "60%", width: "100%", margin: "0 auto" }}>
        {/* Adjust the maxWidth as needed */}
        <form onSubmit={form.onSubmit((values) => console.log(values))}>
          <Title
            order={2}
            size="h1"
            style={{ fontFamily: "Greycliff CF, var(--mantine-font-family)" }}
            fw={900}
            ta="center"
          >
            Get in touch
          </Title>

          <SimpleGrid cols={{ base: 1, sm: 2 }} mt="xl">
            <TextInput
              label="Name"
              placeholder="Your name"
              {...form.getInputProps("name")}
            />
            <TextInput
              label="Email"
              placeholder="Your email"
              {...form.getInputProps("email")}
            />
          </SimpleGrid>

          <TextInput
            label="Subject"
            placeholder="Subject"
            mt="md"
            {...form.getInputProps("subject")}
          />
          <Textarea
            label="Message"
            placeholder="Your message"
            mt="md"
            maxRows={10}
            minRows={5}
            autosize
            {...form.getInputProps("message")}
          />

          <Group justify="center" mt="xl">
            <Button type="submit" size="md">
              Send message
            </Button>
          </Group>
        </form>
      </div>
    </div>
  )
}

export default Contact
