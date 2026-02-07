# Carnavacs API - Windows Deployment Guide

This directory contains deployment scripts for Windows Server 2019.

## Deployment Options

### Option 1: IIS Deployment (Recommended for Production)

Deploy the API as an IIS website with automatic management and monitoring.

**Advantages:**
- Better performance and resource management
- Automatic process recycling
- Built-in health monitoring
- Easy SSL/TLS configuration
- Integration with Windows authentication

**Setup:**

```powershell
# First time: Set up Windows Server
.\deploy\setup-windows-server.ps1

# Deploy the application
.\deploy\deploy.ps1

# Subsequent updates (quicker)
.\deploy\deploy.ps1
```

### Option 2: Windows Service Deployment

Run the API as a standalone Windows Service (alternative to IIS).

**Advantages:**
- Simpler setup
- No IIS required
- Good for dedicated API servers
- Automatic restart on failure

**Setup:**

```powershell
# Install as Windows Service
.\deploy\install-as-service.ps1

# Uninstall service
.\deploy\install-as-service.ps1 -Uninstall
```

## Prerequisites

- Windows Server 2019 or later
- Administrator access
- .NET 9.0 ASP.NET Core Runtime (Hosting Bundle)
- SQL Server (or connection to existing SQL Server)

## Quick Start

### 1. Initial Server Setup

Run this **once** on a new server:

```powershell
# Open PowerShell as Administrator
cd C:\path\to\api
.\deploy\setup-windows-server.ps1
```

This will:
- Install IIS and required features
- Check for .NET 9.0 Runtime
- Configure Windows Firewall
- Create deployment directories

### 2. Configure Settings

Copy and edit the configuration file:

```powershell
Copy-Item appsettings.json.sample appsettings.json
notepad appsettings.json
```

**Required Configuration:**

```json
{
  "ConnectionStrings": {
    "Carnaval": "Server=YOUR_SQL_SERVER;Database=Carnaval;User Id=sa;Password=YOUR_PASSWORD;TrustServerCertificate=true"
  },
  "SecretKeys": {
    "ApiKey": "your-secure-api-key-here",
    "ApiKeySecondary": "backup-key-1,backup-key-2",
    "UseSecondaryKey": true
  },
  "Serilog": {
    "WriteTo": [
      {
        "Name": "File",
        "Args": {
          "path": "C:\\inetpub\\wwwroot\\CarnavalAPI\\logs\\log-.txt"
        }
      }
    ]
  }
}
```

### 3. Deploy the Application

```powershell
# Deploy to IIS (default location: C:\inetpub\wwwroot\CarnavalAPI)
.\deploy\deploy.ps1

# Or deploy to custom location
.\deploy\deploy.ps1 -DeployPath "D:\Apps\CarnavalAPI" -Port 8080
```

### 4. Verify Deployment

Open a browser and navigate to:
- Swagger UI: `http://localhost/swagger` or `http://YOUR_SERVER_IP/swagger`
- Health check: `http://localhost/health`

## Deployment Script Options

### deploy.ps1 Parameters

```powershell
.\deploy\deploy.ps1 `
    -Configuration Release `              # Build configuration (Release/Debug)
    -DeployPath "C:\inetpub\wwwroot\CarnavalAPI" `  # Where to deploy
    -SiteName "CarnavalAPI" `             # IIS site name
    -AppPoolName "CarnavalAPIPool" `      # IIS app pool name
    -Port 80 `                            # HTTP port
    -HostName "api.carnaval.com" `        # Optional: specific hostname
    -SkipIISSetup `                       # Skip IIS configuration (update only)
    -RestartOnly                          # Just restart the site
```

**Examples:**

```powershell
# Full deployment
.\deploy\deploy.ps1

# Deploy to custom port
.\deploy\deploy.ps1 -Port 8080

# Just restart (no rebuild/redeploy)
.\deploy\deploy.ps1 -RestartOnly

# Deploy with hostname
.\deploy\deploy.ps1 -HostName "api.mycompany.com" -Port 80

# Update code without reconfiguring IIS
.\deploy\deploy.ps1 -SkipIISSetup
```

### install-as-service.ps1 Parameters

```powershell
.\deploy\install-as-service.ps1 `
    -ServiceName "CarnavalAPI" `          # Windows service name
    -DisplayName "Carnavacs API Service" ` # Display name
    -InstallPath "C:\Services\CarnavalAPI" ` # Installation directory
    -Port 5000 `                          # HTTP port
    -Uninstall                            # Remove the service
```

## Configuration Guide

### IIS Configuration

The deployment script automatically:
- Creates an application pool with no managed runtime (for .NET Core)
- Sets the app pool to AlwaysRunning mode
- Configures proper permissions for the app pool identity
- Creates or updates the IIS website
- Configures bindings for the specified port

### Windows Service Configuration

The service installation script:
- Creates a Windows Service that starts automatically
- Configures automatic restart on failure
- Sets up proper firewall rules
- Runs under LocalSystem account (can be changed manually)

### SSL/HTTPS Setup

For production deployments with HTTPS:

1. **Obtain SSL Certificate** (from your CA or Let's Encrypt)

2. **Import certificate to Windows**:
   ```powershell
   Import-PfxCertificate -FilePath "certificate.pfx" `
       -CertStoreLocation Cert:\LocalMachine\My `
       -Password (ConvertTo-SecureString -String "cert-password" -AsPlainText -Force)
   ```

3. **Add HTTPS binding in IIS**:
   ```powershell
   New-WebBinding -Name "CarnavalAPI" `
       -Protocol https `
       -Port 443 `
       -HostHeader "api.carnaval.com" `
       -SslFlags 1
   ```

## Monitoring and Maintenance

### Check Application Status

```powershell
# IIS Deployment
Get-Website -Name "CarnavalAPI"
Get-WebAppPoolState -Name "CarnavalAPIPool"

# Service Deployment
Get-Service -Name "CarnavalAPI"
```

### View Logs

```powershell
# View latest logs
Get-Content "C:\inetpub\wwwroot\CarnavalAPI\logs\log-*.txt" -Tail 50

# Monitor logs in real-time
Get-Content "C:\inetpub\wwwroot\CarnavalAPI\logs\log-*.txt" -Tail 50 -Wait

# View IIS logs
Get-Content "C:\inetpub\logs\LogFiles\W3SVC1\*.log" -Tail 50
```

### Restart Application

```powershell
# IIS: Quick restart
.\deploy\deploy.ps1 -RestartOnly

# IIS: Manual restart
Restart-WebAppPool -Name "CarnavalAPIPool"

# Service: Restart
Restart-Service -Name "CarnavalAPI"
```

### Update Application

```powershell
# Deploy new version
.\deploy\deploy.ps1

# The script will:
# 1. Build the latest code
# 2. Stop the site/app pool
# 3. Copy new files
# 4. Restart the site/app pool
```

## Troubleshooting

### Application Won't Start

1. **Check .NET Runtime**:
   ```powershell
   dotnet --list-runtimes
   # Should show: Microsoft.AspNetCore.App 9.0.x
   ```

2. **Check Event Viewer**:
   - Open Event Viewer
   - Navigate to: Windows Logs > Application
   - Look for errors from "IIS AspNetCore Module" or your service name

3. **Check IIS App Pool Identity Permissions**:
   ```powershell
   icacls "C:\inetpub\wwwroot\CarnavalAPI"
   # Should show: IIS AppPool\CarnavalAPIPool:(OI)(CI)(RX)
   ```

### Port Already in Use

```powershell
# Find what's using the port
Get-NetTCPConnection -LocalPort 80

# Stop the conflicting process or deploy to different port
.\deploy\deploy.ps1 -Port 8080
```

### SQL Server Connection Issues

1. **Test connection from PowerShell**:
   ```powershell
   Test-NetConnection -ComputerName "sql-server-name" -Port 1433
   ```

2. **Check SQL Server authentication**:
   - Ensure SQL Server authentication is enabled
   - Verify user has proper database permissions
   - Check firewall on SQL Server

3. **Verify connection string** in `appsettings.json`:
   ```json
   "ConnectionStrings": {
     "Carnaval": "Server=SERVER_NAME;Database=Carnaval;User Id=USERNAME;Password=PASSWORD;TrustServerCertificate=true;Encrypt=true"
   }
   ```

### Logs Not Writing

1. **Check directory permissions**:
   ```powershell
   icacls "C:\inetpub\wwwroot\CarnavalAPI\logs"
   ```

2. **Grant write permission to IIS App Pool**:
   ```powershell
   $path = "C:\inetpub\wwwroot\CarnavalAPI\logs"
   $acl = Get-Acl $path
   $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
       "IIS AppPool\CarnavalAPIPool", "Modify", "Allow"
   )
   $acl.AddAccessRule($rule)
   Set-Acl $path $acl
   ```

### After Installing .NET Hosting Bundle

Always restart IIS after installing the .NET Hosting Bundle:

```powershell
Restart-Service W3SVC
# Or restart the entire server
Restart-Computer
```

## Security Best Practices

1. **Use HTTPS in production** (configure SSL certificate)
2. **Change default API keys** in appsettings.json
3. **Use Windows Authentication** for SQL Server when possible
4. **Enable Windows Firewall** and restrict ports
5. **Keep .NET Runtime updated** for security patches
6. **Use separate accounts** for IIS app pools in production
7. **Encrypt sensitive config** using DPAPI or Azure Key Vault

## Performance Tuning

### IIS App Pool Settings

```powershell
# Increase queue length for high traffic
Set-ItemProperty "IIS:\AppPools\CarnavalAPIPool" -Name "queueLength" -Value 5000

# Set maximum worker processes (for multi-core servers)
Set-ItemProperty "IIS:\AppPools\CarnavalAPIPool" -Name "processModel.maxProcesses" -Value 4

# Increase memory limit
Set-ItemProperty "IIS:\AppPools\CarnavalAPIPool" -Name "recycling.periodicRestart.memory" -Value 2097152
```

### Connection Pool Settings

In `appsettings.json`, add to connection string:
```
;Min Pool Size=10;Max Pool Size=100;Pooling=true
```

## Uninstalling

### Remove IIS Deployment

```powershell
# Remove website
Remove-Website -Name "CarnavalAPI"

# Remove app pool
Remove-WebAppPool -Name "CarnavalAPIPool"

# Remove files (optional)
Remove-Item "C:\inetpub\wwwroot\CarnavalAPI" -Recurse -Force
```

### Remove Service Deployment

```powershell
.\deploy\install-as-service.ps1 -Uninstall

# Remove files (optional)
Remove-Item "C:\Services\CarnavalAPI" -Recurse -Force
```

## Support

For issues or questions:
- Check Event Viewer for detailed error messages
- Review application logs in the logs directory
- Verify all prerequisites are installed
- Ensure SQL Server is accessible and credentials are correct
