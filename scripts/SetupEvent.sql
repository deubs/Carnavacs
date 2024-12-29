DECLARE @espId INT

declare @current varchar(25)
declare @c int
declare @start datetime

declare @noches table (f datetime)

set @start= DATEFROMPARTS(2025,1,4)
set @start= dateadd(hour,21, @start)

INSERT @noches SELECT @start UNION SELECT @start+7 UNION SELECT @start+14 UNION SELECT @start+21 UNION --enero
SELECT @start+28 UNION SELECT @start+35 UNION SELECT @start+42 UNION SELECT @start+49 --febrero
UNION SELECT @start+56 UNION SELECT @start+57 UNION SELECT @start+58 --MARZO



set @current = 'Edicion Carnaval '+trim(str(year(@start)))

IF NOT EXISTS (select * from Espectaculos WHERE Nombre=@current)
	INSERT Espectaculos (nombre, habilitado) values (@current, 1)

SELECT @espId = id from Espectaculos WHERE Nombre=@current;


insert eventos (fecha, fechafin, habilitado, EspectaculoFk, nombre, VisibleWeb)
SELECT f,DATEADD(hour, 6, f),1,@espId, trim(str(ROW_NUMBER() OVER(ORDER BY f)))+ ' Noche de Carnaval del Pais',0
FROM  @noches WHERE NOT EXISTS (SELECT * FROM EVENTOS WHERE FECHA=F);


UPDATE Eventos SET Habilitado=0 WHERE EspectaculoFk<>@espId

IF NOT EXISTS(SELECT *
          FROM   INFORMATION_SCHEMA.COLUMNS
          WHERE  TABLE_NAME = 'PuertaIngreso'
                 AND COLUMN_NAME = 'Enabled') 
ALTER TABLE PuertaIngreso ADD [Enabled] BIT NOT NULL DEFAULT 0;

SELECT * FROM PUERTAINGRESO

UPDATE PuertaIngreso SET Enabled = 1 WHERE Nombre IN ('Puerta 2', 'Puerta 3', 'Puerta 4', 'Puerta 8')


