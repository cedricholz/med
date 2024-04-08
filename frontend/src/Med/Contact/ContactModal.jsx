import React, { useEffect, useState } from "react"
import Modal from "../../components/core/Modal/Modal"
import Contact from "./Contact"

const ContactModal = ({
  active,
  setActive,
  starterMessage,
  backgroundColor,
}) => {
  return (
    <Modal
      backgroundColor={"#f5f5f5"}
      active={active}
      setActive={setActive}
      width={"100%"}
      height={"100%"}
      title={"Contact"}
    >
      <div style={{ width: "100%", height: "100%" }}>
        <Contact
          starterMessage={starterMessage}
          onSuccess={() => {
            setActive(false)
          }}
        />
      </div>
    </Modal>
  )
}

export default ContactModal
