-- Migration: Add TicketType column to QREntradasLecturas table
-- This column stores the ticket type/sector from Quentro API for sector statistics

IF NOT EXISTS (
    SELECT * FROM sys.columns
    WHERE object_id = OBJECT_ID(N'[dbo].[QREntradasLecturas]')
    AND name = 'TicketType'
)
BEGIN
    ALTER TABLE [dbo].[QREntradasLecturas]
    ADD [TicketType] NVARCHAR(100) NULL;

    PRINT 'Column TicketType added to QREntradasLecturas';
END
ELSE
BEGIN
    PRINT 'Column TicketType already exists in QREntradasLecturas';
END
GO
