-- Add friendly name column to AccesosDispositivos
-- NroSerie stores the device IP; NombreAmigable stores the human-readable name

IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'AccesosDispositivos' AND COLUMN_NAME = 'NombreAmigable'
)
BEGIN
    ALTER TABLE [dbo].[AccesosDispositivos]
    ADD [NombreAmigable] NVARCHAR(50) NULL;
END
GO

-- Populate friendly names based on device IPs (from dashboard turnstile config)
UPDATE [dbo].[AccesosDispositivos] SET [NombreAmigable] = CASE [NroSerie]
    WHEN '192.168.40.201' THEN 'tango01'
    WHEN '192.168.40.202' THEN 'tango02'
    WHEN '192.168.40.203' THEN 'tango03'
    WHEN '192.168.40.204' THEN 'tango04'
    WHEN '192.168.40.205' THEN 'tango05'
    WHEN '192.168.40.206' THEN 'tango06'
    WHEN '192.168.40.207' THEN 'tango07'
    WHEN '192.168.40.208' THEN 'tango08'
    WHEN '192.168.40.209' THEN 'tango09'
    WHEN '192.168.40.210' THEN 'tango10'
    WHEN '192.168.40.211' THEN 'tango11'
    WHEN '192.168.40.212' THEN 'tango12'
    WHEN '192.168.40.213' THEN 'tango13'
    WHEN '192.168.40.214' THEN 'raspibalizaproveedores'
    WHEN '192.168.40.215' THEN 'tango15'
    WHEN '192.168.40.216' THEN 'raspi16'
    WHEN '192.168.40.217' THEN 'raspi17'
    WHEN '192.168.40.218' THEN 'tango18'
    WHEN '192.168.40.219' THEN 'tango19'
    WHEN '192.168.40.220' THEN 'tango20'
    WHEN '192.168.40.221' THEN 'baliza-disca'
    WHEN '192.168.40.222' THEN 'vehiculos'
    ELSE [NombreAmigable]
END
WHERE [NroSerie] IN (
    '192.168.40.201','192.168.40.202','192.168.40.203','192.168.40.204',
    '192.168.40.205','192.168.40.206','192.168.40.207','192.168.40.208',
    '192.168.40.209','192.168.40.210','192.168.40.211','192.168.40.212',
    '192.168.40.213','192.168.40.214','192.168.40.215','192.168.40.216',
    '192.168.40.217','192.168.40.218','192.168.40.219','192.168.40.220',
    '192.168.40.221','192.168.40.222'
);
GO
