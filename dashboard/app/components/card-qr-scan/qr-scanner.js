"use client"

import { Html5Qrcode } from "html5-qrcode";
import { store_ticket_validate } from "@/app/stores/ticket_validate";
import { store_API_URL } from "@/app/stores/API_URL";

import { check_ticket } from "@/app/components/utils/scan_qr";
import Qr_information from "@/app/components/card-qr-scan/components/information";

import Button from "@/app/components/common/button";
import Card from "@/app/components/common/card";

export default function Qr_scanner () {

    const { set_data } = store_ticket_validate() 
    const { API_URL } = store_API_URL()

    const check_qr_validation = async (decodedText) => { 
        set_data({ 
            m1: "",
            m2: "",
            info: `Escaneando código ${decodedText}`
        })
        await check_ticket(API_URL, decodedText, set_data) 
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
                    if (devices.indexOf(device) == devices.length -1) {
                        alert("Cámara trasera no detectada, probando cámara delantera")                        
                        cameraId = device.id
                    }
                }

                const html5QrCode = new Html5Qrcode("reader")
                    html5QrCode.start( cameraId,
                        {
                            fps: 15,    // Optional, frame per seconds for qr code scanning
                            qrbox: { width: 300, height: 300 }  // Optional, if you want bounded box UI
                        },
                        (decodedText, decodedResult) => {
                            check_qr_validation(decodedText)
                            html5QrCode.stop()
                        },
                        (errorMessage) => {
                            throw errorMessage
                    })
                    .catch((error) => {
                        throw error
                    })
            } else {
                throw "error obteniendo acceso a alguna cámara"
            }
        }).catch((error) => {
            set_data({ 
                m1: "", 
                m2: "", 
                info: "Error en componente get cameras: ",error})
        });
    }

    return <Card>
        <h3>VALIDAR CÓDIGO QR</h3>
        <div id="reader" width="600"></div>
        <Button text={"Escanear código QR"} callback={scanner_2} />
        <Qr_information />
        </Card>
}
