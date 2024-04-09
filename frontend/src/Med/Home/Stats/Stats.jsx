import React from "react"

import "./Stats.css"

import { Text } from "@mantine/core"
const data = [
  {
    title: "Page views",
    stats: "456,133",
    description:
      "24% more than in the same month last year, 33% more that two years ago",
  },
  {
    title: "New users",
    stats: "2,175",
    description:
      "13% less compared to last month, new user engagement up by 6%",
  },
  {
    title: "Completed orders",
    stats: "1,994",
    description: "1994 orders were completed this month, 97% satisfaction rate",
  },
]
const Stats = () => {
  const stats = data.map((stat) => (
    <div key={stat.title} className={"stat"}>
      <Text>
        <div className={"statCount"}>{stat.stats}</div>
      </Text>
      <Text>
        <div className={"statTitle"}>{stat.title}</div>
      </Text>
      <Text>
        <div className={"statDescription"}>{stat.description}</div>
      </Text>
    </div>
  ))

  return <div className={"statRoot"}>{stats}</div>
}

export default Stats
