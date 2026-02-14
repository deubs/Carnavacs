USE [Carnaval]
GO

/****** Object:  Table [dbo].[Usuarios_Roles]    Script Date: 2/14/2026 4:24:44 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Usuarios_Roles](
	[UserFk] [int] NOT NULL,
	[RoleFk] [int] NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Usuarios_Roles]  WITH CHECK ADD  CONSTRAINT [FK_Usuarios_Roles_Roles] FOREIGN KEY([RoleFk])
REFERENCES [dbo].[Roles] ([Id])
GO

ALTER TABLE [dbo].[Usuarios_Roles] CHECK CONSTRAINT [FK_Usuarios_Roles_Roles]
GO

ALTER TABLE [dbo].[Usuarios_Roles]  WITH CHECK ADD  CONSTRAINT [FK_Usuarios_Roles_Usuarios] FOREIGN KEY([UserFk])
REFERENCES [dbo].[Usuarios] ([Id])
GO

ALTER TABLE [dbo].[Usuarios_Roles] CHECK CONSTRAINT [FK_Usuarios_Roles_Usuarios]
GO


