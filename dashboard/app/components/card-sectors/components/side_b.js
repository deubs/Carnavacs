"use client"
import css from "@/app/styles/events_sector_stats_side_b.module.css"

import { store_events_sector_stats } from "@/app/stores/events_sector_stats"
import { Sector_stats_area } from "@/app/components/card-sectors/components/components/card"
import { useEffect, useState } from "react"

export default function Side_B () {
  const { sector_stats } = store_events_sector_stats()
  const [ data_site, set_data_site ] = useState([
    {
        name: "Popular",
        type: "TRIBUNA",
        sector: "POPULAR",
        quantity: 0
    },
    {
        name: "SSILLAS1B",
        type: "SILLAS",
        sector: "1B",
        quantity: 0
    },
    {
        name: "SSILLAS2B",
        type: "SILLAS",
        sector: "2B",
        quantity: 0
    },
    {
        name: "SSILLAS3B",
        type: "SILLAS",
        sector: "3B",
        quantity: 0
    },
    {
        name: "SVIPRE",
        type: "SECTOR VIP",
        sector: "ROSADO ESTE",
        quantity: 0
    },
    {
        name: "SVIPRC",
        type: "SECTOR VIP",
        sector: "ROSADO CENTRO",
        quantity: 0
    },
    {
        name: "SVIPRO",
        type: "SECTOR VIP",
        sector: "ROSADO OESTE",
        quantity: 0
    },
    {
        name: "SSILLAS4B",
        type: "SILLAS",
        sector: "4B",
        quantity: 0
    },
    {
        name: "SSILLAS5B",
        type: "SILLAS",
        sector: "5B",
        quantity: 0
    },
    {
        name: "SVIP5B",
        type: "SILLAS VIP",
        sector: "5B",
        quantity: 0
    },
    {
        name: "SVIP6B",
        type: "SILLAS VIP",
        sector: "6B",
        quantity: 0
    },
    {
        name: "SSILLAS6B",
        type: "SILLAS",
        sector: "6B",
        quantity: 0
    },
    {
        name: "SSILLAS7B",
        type: "SILLAS",
        sector: "7B",
        quantity: 0
    }  
  ])

  useEffect(()=>{
  if (sector_stats != "loading") {

    let data_updated = []
    for (let sector of data_site) {
      //console.log(`iterando en el sector ${sector.type} ${sector.sector}`)
      try {
          let sector_copy = sector;
          const target = sector_stats.filter(item => item.name == sector_copy.name)
          if (target.length) sector_copy.quantity = target[0].total
          data_updated.push(sector_copy)

      } catch (error) {
          console.log(error)
      }
  }
  set_data_site(data_updated)
  }
  
},[sector_stats])

    return <div className={css.main}>
      {
        data_site.map(data_site => <Sector_stats_area data={ data_site } key={data_site.name}/>)
      }
    </div>
} 