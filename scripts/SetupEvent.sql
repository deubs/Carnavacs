DECLARE @espId INT

declare @current varchar(25)
declare @c int
declare @start datetime

declare @noches table (f datetime)

set @start= DATEFROMPARTS(2026,1,3)
set @start= dateadd(hour,21, @start)

INSERT @noches SELECT @start UNION SELECT @start+7 UNION SELECT @start+14 UNION SELECT @start+21 UNION --enero
SELECT @start+28 UNION SELECT @start+35 UNION SELECT @start+42 UNION SELECT @start+43 UNION SELECT @start+44 UNION
SELECT @start+49 UNION SELECT @start+56 

SELECT* FROM  @NOCHES

set @current = 'Edicion Carnaval '+RTRIM(Ltrim(str(year(@start))))

IF NOT EXISTS (select * from Espectaculos WHERE Nombre=@current)
	INSERT Espectaculos (nombre, habilitado) values (@current, 1)

SELECT @espId = id from Espectaculos WHERE Nombre=@current;


insert eventos (fecha, fechafin, habilitado, EspectaculoFk, nombre, VisibleWeb)
SELECT f,DATEADD(hour, 6, f),1,@espId, LTRIM(RTrim(str(ROW_NUMBER() OVER(ORDER BY f))))+ ' Noche de Carnaval del Pais',0
FROM  @noches WHERE NOT EXISTS (SELECT * FROM EVENTOS WHERE FECHA=F);


UPDATE Eventos SET Habilitado=0 WHERE EspectaculoFk<>@espId


UPDATE PuertaIngreso SET Enabled = 1 WHERE Nombre IN ('Puerta 2', 'Puerta 3', 'Puerta 4', 'Puerta 8')

--invitados
insert eventos_tipoEntradas (eventofk, TipoEntradaFk,precio, visible, visibleweb, vigencia,quota)
select id,24,0,1,0,'2027-03-10',1 from eventos where EspectaculoFk=@espId

update Eventos_TipoEntradas set Vigencia='2027-01-01' where vigencia is null
