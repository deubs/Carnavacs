"use client"
import 'chart.js/auto';
import styles from "@/app/styles/charts.module.css"
import { Line } from 'react-chartjs-2';
import { store_stats_all_nights } from "@/app/stores/stats_all_nights";
import { useEffect, useState } from "react";   
import { store_events_stats } from '@/app/stores/events_stats';
 
export default function Chart () {

  const { previous_nights, actually_night, set_actually_night } = store_stats_all_nights()
  const { events_stats } = store_events_stats()
  const [ nights, set_nights ] = useState([])
  const [ quantities, set_quantities ] = useState([])

  useEffect(()=>{
    const updated_tickets_quantity = events_stats.totalTickets || 0;
    set_actually_night({
      id: actually_night.id,
      name: actually_night.name,
      quantity: updated_tickets_quantity
    })
  }, [events_stats]) 

  useEffect(()=>{
    if (previous_nights?.length > 0) {
      const order_array = previous_nights.sort((a,b) => a.timestamp - b.timestamp)
      const _nights = order_array.map(item=>item.name)
      const _quantities = order_array.map(item=>item.quantity)
      set_nights(_nights)
      set_quantities(_quantities)
    }
  }, [previous_nights])

    const _data = {
        labels: [...nights, actually_night.name],
        datasets: [
            {
                label: 'Tickets vendidos',
                data: [...quantities, actually_night.quantity],
                fill: { target: 'origin', above: 'rgba(75,192,192,0.4)', below: 'rgba(75,192,192,0.1)' },
                borderColor: 'green',
                tension: 0
            }
        ]
    };
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: { ticks: { color: 'white' }},
            y: { ticks: { color: 'white' }}
          },
          legend: {
            labels: {
              color: 'white' // Color del label del dataset
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
    };
    return <div className={styles.line_chart}>
    <Line
    data={_data}
    options={options}
    />
    </div>
}