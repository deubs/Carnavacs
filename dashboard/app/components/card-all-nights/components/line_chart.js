"use client"
import styles from "@/app/styles/charts.module.css"
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import { store_all_stats } from "@/app/stores/stats_all_nights";
import { useEffect, useState } from "react";

export default function Chart () {
    const { data } = store_all_stats()
    const [ nights, set_nights ] = useState(["cargando..."])
    const [ quantitys, set_quantitys ] = useState(["cargando..."])

    useEffect(()=>{

        const _nights = data.map(night => night.nombre)
        console.log(_nights)
        const _quantitys = data.map(night => night.quantity)
        set_nights(_nights)
        set_quantitys(_quantitys)

    }, [data])

    const _data = {
        labels: nights,
        datasets: [
            {
                label: 'Tickets vendidos',
                data: quantitys,
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
    <Line
    data={_data}
    options={options}
    />
    </div>
}

