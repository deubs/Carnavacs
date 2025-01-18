"use client"

import { useEffect, useRef, useState } from 'react';

export default function QRReader() {
  const videoRef = useRef(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const test = () => {
    if (typeof window !== 'undefined' && window.navigator && window.navigator.mediaDevices) {
      alert("yet")
      navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(stream => {
          const video = videoRef.current;
          if (video) {
            video.srcObject = stream;
            video.play();

            const interval = setInterval(() => {
              const imageData = video.getContext('2d').getImageData(0, 0, video.videoWidth, video.videoHeight);
              const code = jsQR(imageData.data, imageData.width, imageData.height);
              if (code) {
                setResult(code.data);
                clearInterval(interval); // Detener el intervalo después de encontrar un código
              }
            }, 500); 

            return () => clearInterval(interval); // Limpiar el intervalo al desmontar el componente
          }
        })
        .catch(error => {
          setError('Error al acceder a la cámara: ' + error.message);
        });
    }
  }

  return (
    <div>
      {error && <p>{error}</p>}
      <video ref={videoRef} width="320" height="240" />
      {result && <p>Resultado: {result}</p>}
      {/* Resto del componente */}
      <button onClick={()=>test()}>test</button>
    </div>
  );
}