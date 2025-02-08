"use client"
import css from "@/app/styles/qr_scanner.module.css"

import { Html5QrcodeScanner } from "html5-qrcode";
import { Html5Qrcode } from "html5-qrcode";
import { store_ticket_validate } from "@/app/stores/ticket_validate";
import { store_API_URL } from "@/app/stores/API_URL";

import { check_ticket } from "@/app/querys/scan_qr";
import { QRCODE_information } from "@/app/components/tickets/QRCODE_information";

import Button from "../common/Button";

export default function Qr_scanner () {

    const { set_data } = store_ticket_validate()
    const { API_URL } = store_API_URL()

    function onScanSuccess(decodedText, decodedResult) {
    // handle the scanned code as you like, for example:
    console.log(`Code matched = ${decodedText}`, decodedResult);
    }
    function onScanFailure(error) {
    // handle scan failure, usually better to ignore and keep scanning.
    console.warn(`Code scan error = ${error}`);
    }
    
    const scanner_1 = () => {
      let html5QrcodeScanner = new Html5QrcodeScanner(
        "reader",
        { fps: 10, qrbox: {width: 250, height: 250} },
        false);
        html5QrcodeScanner.render(onScanSuccess, onScanFailure)
    }

    // -----------------------------------------------------------
    // actualizar estados segun el retorno de la validacion del qr
    // -----------------------------------------------------------

    const check_qr_validation = async (decodedText) => {
        const r = await check_ticket(API_URL, decodedText, set_data)
    }
    const scanner_2 = () => {
        Html5Qrcode.getCameras().
        then(devices => {
            let cameraId;
    
            if (devices && devices.length) {
                // buscar camara trasera
                for (const device of devices) {
                    if (device.label.toLowerCase().includes("back") || device.label.toLowerCase().includes("rear")) {
                        cameraId = device.id
                        break;
                    }
                }
                // inicializar la camara que busca

                if (cameraId) {
                    const html5QrCode = new Html5Qrcode("reader")
                    html5QrCode.start( cameraId,
                        {
                            fps: 15,    // Optional, frame per seconds for qr code scanning
                            qrbox: { width: 300, height: 300 }  // Optional, if you want bounded box UI
                        },
                        (decodedText, decodedResult) => {
                            check_qr_validation(decodedText)
                        },
                        (errorMessage) => {
                            throw errorMessage
                    })
                    .catch((error) => {
                        console.log(error)
                    })
                }
            }
        }).catch(err => {
            set_data({ m1: "Error", m2: "Error", info: "Error obteniendo acceso a la cámara"})
        });
    }

    return <div className={css.main}>
        <div id="reader" width="600"></div>
        <QRCODE_information />
        <Button texto={"Escanear código QR"} onClick={scanner_2} />
        </div>
}

/*
<Button texto={"Escanear QR"} onClick={scanner_1} />
*/