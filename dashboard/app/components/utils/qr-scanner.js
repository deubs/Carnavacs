"use client"
import css from "@/app/styles/qr_scanner.module.css"

import { Html5QrcodeScanner } from "html5-qrcode";
import { Html5Qrcode } from "html5-qrcode";
import { store_notification } from "@/app/stores/notification";
import { store_ticket_validate } from "@/app/stores/ticket_validate";

import { check_ticket } from "@/app/hooks/scan_qr";

import Ticket_validate from "../tickets/validate";

import Button from "../common/Button";

export default function Qr_scanner () {
    const { set_message } = store_notification()
    const { set_data } = store_ticket_validate()

    function onScanSuccess(decodedText, decodedResult) {
    // handle the scanned code as you like, for example:
    console.log(`Code matched = ${decodedText}`, decodedResult);
    }
    function onScanFailure(error) {
    // handle scan failure, usually better to ignore and keep scanning.
    console.warn(`Code scan error = ${error}`);
    }
    const scan_2 = () => {
      let html5QrcodeScanner = new Html5QrcodeScanner(
        "reader",
        { fps: 10, qrbox: {width: 250, height: 250} },
        false);
        html5QrcodeScanner.render(onScanSuccess, onScanFailure)
    }
    const scan_1 = () => {
        Html5Qrcode.getCameras().then(devices => {
            if (devices && devices.length) {
                var cameraId = devices[0].id;
                const html5QrCode = new Html5Qrcode(/* */ "reader");
                html5QrCode.start(
                    cameraId,
                    {
                        fps: 15,    // Optional, frame per seconds for qr code scanning
                        qrbox: { width: 300, height: 300 }  // Optional, if you want bounded box UI
                    },
                    (decodedText, decodedResult) => {
                        const check = async () => {
                            const r = await check_ticket(decodedText)
                            if(r.success){
                                set_data({ m1: r.result.m1, m2: r.result.m2 })
                            }
                        }
                        check()
                    },
                    (errorMessage) => {})
                    .catch((err) => {
                        // handlear error
                        console.log(err)
            })}
        }).catch(err => { alert("no device") });
    }

    return <div className={css.main}>
        <Button texto={"Escanear QR"} onClick={scan_1} />
        <Button texto={"Cargar imagen"} onClick={scan_2} />
        <div id="reader" width="600"></div>
        <Ticket_validate />
        </div>
}