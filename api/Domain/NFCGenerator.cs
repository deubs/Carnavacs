
using System;
using System.IO;
using Carnavacs.Api.Controllers;
using Carnavacs.Api.Domain.Interfaces;
using Microsoft.Extensions.Logging;
using NdefLibrary.Ndef;
namespace Carnavacs.Api.Domain
{
    public class NFCGenerator : INFCGenerator
    {
        private readonly ILogger<NFCGenerator> _logger;

        public NFCGenerator(ILogger<NFCGenerator> logger)
        {
            _logger = logger;
        }


        public string Get()
        {

            // Información única para cada cliente
            string clienteNombre = "Juan Perez";
            string eventoInfo = "Carnaval de Gualeguaychú 2024";
            string ticketId = Guid.NewGuid().ToString(); // Genera un ID único para el boleto
            string nfcFilePath = Path.Combine(Path.GetTempPath(), ticketId);
            try
            {

                // Crear el mensaje NFC
                var nfcMessage = new NdefMessage();
                var textRecord = new NdefTextRecord
                {
                    Text = $"{clienteNombre} - {eventoInfo} - ID: {ticketId}",
                    LanguageCode = "es"
                };
                nfcMessage.Add(textRecord);

                // Guardar el mensaje NFC en un archivo
                File.WriteAllBytes(nfcFilePath, nfcMessage.ToByteArray());

                Console.WriteLine("¡Archivo NFC generado exitosamente! Ubicación: " + nfcFilePath);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }

            return nfcFilePath;
        }
    }
}