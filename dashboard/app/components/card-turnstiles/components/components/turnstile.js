"use client"
import styles from "@/app/styles/turnstile.module.css"

export default function Turnstile ({ data }) {
    return <>
    {
        data && <div className={styles.main}>
            <div className={styles.title}>
                <p>MOLINETE</p>
                <p className={styles.number}>{data.deviceName.slice(-2)}</p>
            </div>
            <div className={styles.content}>
                <p>INGRESOS</p>
                <p className={styles.number}>{data.peopleCount}</p>
            </div>
    </div>
    }
    </>
} 