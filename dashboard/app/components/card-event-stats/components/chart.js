"use client"
import styles from "@/app/styles/charts.module.css"
import { store_events_stats } from "@/app/stores/events_stats"


import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

export default function Tickets_quantity_chart () {
  const { events_stats } = store_events_stats()

  const data = {
    labels: ['Tickets totales', 'Tickets usados', 'Tickets pendientes'],
    datasets: [{
      data: [events_stats.totalTickets, events_stats.usedTickets, events_stats.remainingTickets],
      backgroundColor: 'rgba(75,192,192,0.4)',
      borderColor: 'green',
      borderWidth: 3,
    }]
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

    return <div className={styles.chart_bar}>
    <Bar
    data={data}
    options={options}
    />
    </div>
}


