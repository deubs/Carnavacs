"use client"
import { useEffect } from "react"
import css from "@/app/test/test.module.css"
import Sector_stats_side_A from "../components/events/sector_stats_side_A"
import Sector_stats_side_B from "../components/events/sector_stats_side_B"

const response = [{
    "id": 0,
    "name": "Popular",
    "total": "9002",
    "readed": "8416"
  },
  {
    "id": 0,
    "name": "SPBV",
    "total": "48",
    "readed": "44"
  },
  {
    "id": 0,
    "name": "SPESTE",
    "total": "32",
    "readed": "18"
  },
  {
    "id": 0,
    "name": "SPOESTE",
    "total": "312",
    "readed": "301"
  },
  {
    "id": 0,
    "name": "SSILLAS1A",
    "total": "122",
    "readed": "116"
  },
  {
    "id": 0,
    "name": "SSILLAS2A",
    "total": "165",
    "readed": "161"
  },
  {
    "id": 0,
    "name": "SSILLAS2B",
    "total": "181",
    "readed": "175"
  },
  {
    "id": 0,
    "name": "SSILLAS3A",
    "total": "175",
    "readed": "172"
  },
  {
    "id": 0,
    "name": "SSILLAS3B",
    "total": "205",
    "readed": "199"
  },
  {
    "id": 0,
    "name": "SSILLAS4A",
    "total": "386",
    "readed": "364"
  },
  {
    "id": 0,
    "name": "SSILLAS4B",
    "total": "389",
    "readed": "366"
  },
  {
    "id": 0,
    "name": "SSILLAS5A",
    "total": "169",
    "readed": "169"
  },
  {
    "id": 0,
    "name": "SSILLAS5B",
    "total": "219",
    "readed": "212"
  },
  {
    "id": 0,
    "name": "SSILLAS6A",
    "total": "55",
    "readed": "52"
  },
  {
    "id": 0,
    "name": "SSILLAS6B",
    "total": "135",
    "readed": "128"
  },
  {
    "id": 0,
    "name": "SSILLAS7A",
    "total": "21",
    "readed": "20"
  },
  {
    "id": 0,
    "name": "SSILLAS7B",
    "total": "26",
    "readed": "26"
  },
  {
    "id": 0,
    "name": "SVIP5B",
    "total": "98",
    "readed": "98"
  },
  {
    "id": 0,
    "name": "SVIP6A",
    "total": "68",
    "readed": "67"
  },
  {
    "id": 0,
    "name": "SVIP6B",
    "total": "64",
    "readed": "61"
  },
  {
    "id": 0,
    "name": "SVIPNEW",
    "total": "92",
    "readed": "91"
  },
  {
    "id": 0,
    "name": "SVIPRC",
    "total": "124",
    "readed": "104"
  },
  {
    "id": 0,
    "name": "SVIPRE",
    "total": "246",
    "readed": "188"
  },
  {
    "id": 0,
    "name": "SVIPRO",
    "total": "278",
    "readed": "238"
  },
  {
    "id": 0,
    "name": "SVIPTC",
    "total": "670",
    "readed": "631"
  },
  {
    "id": 0,
    "name": "SVIPTE",
    "total": "216",
    "readed": "203"
  },
  {
    "id": 0,
    "name": "SVIPTO",
    "total": "228",
    "readed": "218"
  }]

export default function Test () {
    const doc_site_A = [
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
            name: "SVIPNEW",
            type: "SECTOR VIP",
            sector: "VIP NUEVO",
            quantity: 0
        },
        {
            name: "SVIP6A",
            type: "SILLAS VIP",
            sector: "4A",
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
    ]
    return <>
    <Sector_stats_side_A />
    <Sector_stats_side_B />
    </>
} 

/*

        <div className={css.top}></div>
        <details className={css.details}>
            <summary className={css.summary}>Detalles</summary>
            <ul>
                <li>item 1</li>
                <li>item 1</li>
                <li>item 1</li>
                <li>item 1</li>
                <li>item 1</li>
            </ul>
        </details>
        <div className={css.bottom}></div>
*/

/*
<div className={css.main}> 
        <div className={css.norte}>
            <div className={css.sector}>
                <p>7B</p>
            </div>
            <div className={css.sector}>
                <p>6B</p>
            </div>
            <div className={css.sector}>
                <p>6BVIP</p>
            </div>
            <div className={css.sector}>
                <p>5BV</p>
            </div>
            <div className={css.sector}>
                <p>5B</p>
            </div>
            <div className={css.sector}>
                <p>4B</p>
            </div>
            <div className={css.sector}>
                <p>VRO</p>
            </div>
            <div className={css.sector}>
                <p>VRC</p>
            </div>
            <div className={css.sector}>
                <p>VRE</p>
            </div>
            <div className={css.sector}>
                <p>3B</p>
            </div>
            <div className={css.sector}>
                <p>2B</p>
            </div>
            <div className={css.sector}>
                <p>1B</p>
            </div>
        </div>
        <div className={css.sur}>
            <div className={css.sector}>
                <p>7A</p>
            </div>
            <div className={css.sector}>
                <p>6A</p>
            </div>
            <div className={css.sector}>
                <p>6AVIP</p>
            </div>
            <div className={css.sector}>
                <p>VN</p>
            </div>
            <div className={css.sector}>
                <p>5A</p>
            </div>
            <div className={css.sector}>
                <p>4A</p>
            </div>
            <div className={css.sector}>
                <p>VTC</p>
            </div>
            <div className={css.sector}>
                <p>VTC</p>
            </div>
            <div className={css.sector}>
                <p>VTE</p>
            </div>
            <div className={css.sector}>
                <p>3A</p>
            </div>
            <div className={css.sector}>
                <p>2A</p>
            </div>
            <div className={css.sector}>
                <p>1A</p>
            </div>
        </div>
        <div className={css.sector_area}>
            <p className={css.sector_indentify}>SILLAS</p>
            <p className={css.sector_name}>7B</p>
            <p className={css.sector_quantity}>1150 INGRESOS</p>
        </div>
    </div>
*/