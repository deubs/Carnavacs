# Carnavacs API Deployment Script for Windows Server
# This script builds and deploys the API to IIS on Windows Server 2019

param(
    [string]$Configuration = "Release",
    [string]$DeployPath = "C:\inetpub\wwwroot\CarnavalAPI",
    [string]$SiteName = "CarnavalAPI",
    [string]$AppPoolName = "CarnavalAPIPool",
    [int]$Port = 80,
    [string]$HostName = "",
    [switch]$SkipIISSetup,
    [switch]$RestartOnly
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warn { Write-Host $args -ForegroundColor Yellow }
function Write-Error { param([string]$Message) Write-Host $Message -ForegroundColor Red }

Write-Info "🚀 Carnavacs API Deployment Script"
Write-Info "=================================="
Write-Info "Configuration: $Configuration"
Write-Info "Deploy Path: $DeployPath"
Write-Info "IIS Site: $SiteName"
Write-Info ""

# Get script directory (where the .csproj is)
$ScriptDir = Split-Path -Parent $PSScriptRoot
$ProjectFile = Join-Path $ScriptDir "Carnavacs.Api.csproj"

if (-not (Test-Path $ProjectFile)) {
    Write-Error "ERROR: Project file not found at $ProjectFile"
    exit 1
}

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Error "ERROR: This script must be run as Administrator"
    Write-Warn "Right-click PowerShell and select 'Run as Administrator'"
    exit 1
}

# If RestartOnly, just restart the app pool and site
if ($RestartOnly) {
    Write-Info "♻️  Restarting IIS site..."
    Import-Module WebAdministration
    
    if (Test-Path "IIS:\AppPools\$AppPoolName") {
        Stop-WebAppPool -Name $AppPoolName
        Start-Sleep -Seconds 2
        Start-WebAppPool -Name $AppPoolName
        Write-Success "✅ App Pool '$AppPoolName' restarted"
    }
    
    if (Test-Path "IIS:\Sites\$SiteName") {
        Stop-Website -Name $SiteName
        Start-Sleep -Seconds 2
        Start-Website -Name $SiteName
        Write-Success "✅ Website '$SiteName' restarted"
    }
    
    Write-Success "`n✅ Restart complete!"
    exit 0
}

# Step 1: Build the application
Write-Info "📦 Building application..."
try {
    $buildOutput = Join-Path $ScriptDir "bin\$Configuration\net9.0-windows\publish"
    
    # Clean previous build
    if (Test-Path $buildOutput) {
        Remove-Item -Path $buildOutput -Recurse -Force
    }
    
    # Build and publish
    dotnet publish $ProjectFile `
        --configuration $Configuration `
        --output $buildOutput `
        --self-contained false `
        --verbosity minimal
    
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed with exit code $LASTEXITCODE"
    }
    
    Write-Success "✅ Build successful"
} catch {
    Write-Error "ERROR: Build failed - $_"
    exit 1
}

# Step 2: Stop IIS site if it exists
Write-Info "🛑 Stopping IIS site..."
try {
    Import-Module WebAdministration
    
    if (Test-Path "IIS:\Sites\$SiteName") {
        Stop-Website -Name $SiteName
        Write-Info "Stopped website: $SiteName"
    }
    
    if (Test-Path "IIS:\AppPools\$AppPoolName") {
        Stop-WebAppPool -Name $AppPoolName
        Start-Sleep -Seconds 3  # Wait for app pool to fully stop
        Write-Info "Stopped app pool: $AppPoolName"
    }
} catch {
    Write-Warn "Warning: Could not stop IIS site - $_"
}

# Step 3: Deploy files
Write-Info "📤 Deploying files to $DeployPath..."
try {
    # Create deploy directory if it doesn't exist
    if (-not (Test-Path $DeployPath)) {
        New-Item -ItemType Directory -Path $DeployPath -Force | Out-Null
    }
    
    # Copy files
    Copy-Item -Path "$buildOutput\*" -Destination $DeployPath -Recurse -Force
    
    # Create logs directory
    $logsPath = Join-Path $DeployPath "logs"
    if (-not (Test-Path $logsPath)) {
        New-Item -ItemType Directory -Path $logsPath -Force | Out-Null
    }
    
    Write-Success "✅ Files deployed"
} catch {
    Write-Error "ERROR: Deployment failed - $_"
    exit 1
}

# Step 4: Setup IIS (if not skipped)
if (-not $SkipIISSetup) {
    Write-Info "⚙️  Configuring IIS..."
    try {
        Import-Module WebAdministration
        
        # Create App Pool if it doesn't exist
        if (-not (Test-Path "IIS:\AppPools\$AppPoolName")) {
            Write-Info "Creating application pool: $AppPoolName"
            New-WebAppPool -Name $AppPoolName
            
            # Configure App Pool for .NET Core
            Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name "managedRuntimeVersion" -Value ""
            Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name "startMode" -Value "AlwaysRunning"
            Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name "processModel.idleTimeout" -Value "00:00:00"
        }
        
        # Set proper permissions on deploy folder
        $acl = Get-Acl $DeployPath
        $identity = "IIS AppPool\$AppPoolName"
        $fileSystemRights = [System.Security.AccessControl.FileSystemRights]::ReadAndExecute
        $inheritanceFlags = [System.Security.AccessControl.InheritanceFlags]"ContainerInherit, ObjectInherit"
        $propagationFlags = [System.Security.AccessControl.PropagationFlags]::None
        $type = [System.Security.AccessControl.AccessControlType]::Allow
        
        $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
            $identity, $fileSystemRights, $inheritanceFlags, $propagationFlags, $type
        )
        $acl.AddAccessRule($accessRule)
        Set-Acl $DeployPath $acl
        
        # Create or update website
        if (Test-Path "IIS:\Sites\$SiteName") {
            Write-Info "Updating existing website: $SiteName"
            Set-ItemProperty "IIS:\Sites\$SiteName" -Name "physicalPath" -Value $DeployPath
            Set-ItemProperty "IIS:\Sites\$SiteName" -Name "applicationPool" -Value $AppPoolName
        } else {
            Write-Info "Creating new website: $SiteName"
            
            # Create binding
            if ($HostName) {
                $binding = "*:${Port}:$HostName"
            } else {
                $binding = "*:${Port}:"
            }
            
            New-Website -Name $SiteName `
                -PhysicalPath $DeployPath `
                -ApplicationPool $AppPoolName `
                -Port $Port `
                -HostHeader $HostName
        }
        
        Write-Success "✅ IIS configured"
    } catch {
        Write-Error "ERROR: IIS setup failed - $_"
        Write-Warn "You may need to configure IIS manually"
    }
}

# Step 5: Start the site
Write-Info "▶️  Starting IIS site..."
try {
    if (Test-Path "IIS:\AppPools\$AppPoolName") {
        Start-WebAppPool -Name $AppPoolName
        Write-Info "Started app pool: $AppPoolName"
    }
    
    if (Test-Path "IIS:\Sites\$SiteName") {
        Start-Website -Name $SiteName
        Write-Info "Started website: $SiteName"
    }
    
    Start-Sleep -Seconds 2
    Write-Success "✅ IIS site started"
} catch {
    Write-Error "ERROR: Could not start IIS site - $_"
    exit 1
}

# Step 6: Verify deployment
Write-Info "`n📋 Deployment Summary"
Write-Info "====================="
Write-Info "Deploy Path: $DeployPath"
Write-Info "IIS Site: $SiteName"
Write-Info "App Pool: $AppPoolName"
Write-Info "Port: $Port"
if ($HostName) {
    Write-Info "Host: $HostName"
    Write-Info "URL: http://$HostName`:$Port"
} else {
    Write-Info "URL: http://localhost:$Port"
}

# Check if site is running
try {
    $site = Get-Website -Name $SiteName
    $appPool = Get-WebAppPoolState -Name $AppPoolName
    
    if ($site.State -eq "Started" -and $appPool.Value -eq "Started") {
        Write-Success "`n✅ Deployment successful!"
        Write-Info "`nTo check logs:"
        Write-Info "  Get-Content '$logsPath\log-*.txt' -Tail 50"
    } else {
        Write-Warn "`n⚠️  Deployment completed but site may not be running"
        Write-Info "Site State: $($site.State)"
        Write-Info "App Pool State: $($appPool.Value)"
    }
} catch {
    Write-Warn "Could not verify site status"
}

Write-Info "`nUseful commands:"
Write-Info "  Restart site:  .\deploy.ps1 -RestartOnly"
Write-Info "  View logs:     Get-Content '$logsPath\log-*.txt' -Tail 50 -Wait"
Write-Info "  Check status:  Get-Website -Name $SiteName"
