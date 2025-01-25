"use client"
import css from "./css.module.css"
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

export const LineChart = ({ stats }) => {
    const data = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
        datasets: [
            {
                label: 'Ventas',
                data: [12, 19, 50, 200, 10],
                fill: false,
                borderColor: 'rgb(255, 255, 255)',
                tension: 0.2
            }
        ]
    };
    return <Line
    data={data}
    className={css.chart_line} />
}