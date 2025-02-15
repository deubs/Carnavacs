"use client"
import css from "@/app/styles/events_sector_stats_side_a.module.css"

import { store_events_sector_stats } from "@/app/stores/events_sector_stats"
import { Sector_stats_area } from "@/app/components/card-sectors/components/components/card"
import { useEffect, useState } from "react"

export default function Side_A () {
  const { sector_stats } = store_events_sector_stats()
  const [ data_site, set_data_site ] = useState([
    {
        name: "SSILLAS1A",
        type: "SILLAS",
        sector: "1A",
        quantity: 0
    },
    {
        name: "SSILLAS2A",
        type: "SILLAS",
        sector: "2A",
        quantity: 0
    },
    {
        name: "SPESTE",
        type: "PULLMAN",
        sector: "ESTE",
        quantity: 0
    },
    {
        name: "SSILLAS3A",
        type: "SILLAS",
        sector: "3A",
        quantity: 0
    },
    {
        name: "SVIPTE",
        type: "SECTOR VIP",
        sector: "TRADICIONAL ESTE",
        quantity: 0
    },
    {
        name: "SVIPTC",
        type: "SECTOR VIP",
        sector: "TRADICIONAL CENTRO",
        quantity: 0
    },
    {
        name: "SVIPTO",
        type: "SECTOR VIP",
        sector: "TRADICIONAL OESTE",
        quantity: 0
    },
    {
        name: "SSILLAS4A",
        type: "SILLAS",
        sector: "4A",
        quantity: 0
    },
    {
        name: "SSILLAS5A",
        type: "SILLAS",
        sector: "5A",
        quantity: 0
    },
    {
        name: "SPOESTE",
        type: "PULLMAN",
        sector: "OESTE",
        quantity: 0
    },
    {
        name: "SVIPNEW",
        type: "SECTOR VIP",
        sector: "VIP NUEVO",
        quantity: 0
    },
    {
        name: "SVIP6A",
        type: "SILLAS VIP",
        sector: "6A",
        quantity: 0
    },
    {
        name: "SSILLAS6A",
        type: "SILLAS",
        sector: "6A",
        quantity: 0
    },
    {
        name: "SSILLAS7A",
        type: "SILLAS",
        sector: "7A",
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