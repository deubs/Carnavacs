"use client"
import css from "@/app/styles/charts.module.css"

import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

export const BarChart = ({ stats }) => {
    const data = {
      labels: ['Totales', 'Usados', 'Pendientes'],
      datasets: [
        {
          label: 'Cantidad de ingresos',
          data: [stats[0], stats[1], stats[2]],
          backgroundColor: 'rgba(255,255,255,0.15)',
          borderColor: 'rgba(255,255,255,0.4)',
          borderWidth: 1,
        }
      ]
    };
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: {
              color: 'white' // Cambia el color de las etiquetas del eje X a blanco
            }
          },
          y: {
            ticks: {
              color: 'white' // Cambia el color de las etiquetas del eje Y a blanco
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: 'white' // Color del label del dataset
            }
          }
        }
    }
    return <div className={css.chart_bar}>
    <Bar
    data={data}
    options={options}
    />
    </div>
}


