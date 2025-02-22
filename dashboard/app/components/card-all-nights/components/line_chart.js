"use client"
import 'chart.js/auto';
import styles from "@/app/styles/charts.module.css"
import { Line } from 'react-chartjs-2';
import { store_stats_all_nights } from "@/app/stores/stats_all_nights";
import { store_events_stats } from '@/app/stores/events_stats';
import { useEffect, useState } from "react";   

export default function Chart () {

  const { events_stats } = store_events_stats()
  const { previous_nights } = store_stats_all_nights() 
  const [ nights, set_nights ] = useState([])
  const [ quantities, set_quantities ] = useState([])

  /*
  useEffect(()=>{
    console.log("events stats desde graph: ",events_stats)
    if (events_stats != "loading") {
      
  }, [events_stats])
  */
 
  useEffect(()=>{
    if (previous_nights.length > 0) {
      const _nights = previous_nights.map(item=>item.name)
      const _quantities = previous_nights.map(item=>item.quantity)
      set_nights(_nights)
      set_quantities(_quantities)
    }
  }, [previous_nights])

    const _data = {
        labels: nights,
        datasets: [
            {
                label: 'Tickets vendidos',
                data: quantities,
                fill: { target: 'origin', above: 'rgba(75,192,192,0.4)', below: 'rgba(75,192,192,0.1)' },
                borderColor: 'green',
                tension: 0.2
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
    }
    return <div className={styles.line_chart}>
      <button onClick={()=>{console.log(previous_nights)}}>check</button>
    <Line
    data={_data}
    options={options}
    />
    </div>
}