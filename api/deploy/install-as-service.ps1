# Install Carnavacs API as a Windows Service
# Alternative to IIS deployment - runs as a background Windows Service

param(
    [string]$ServiceName = "CarnavalAPI",
    [string]$DisplayName = "Carnavacs API Service",
    [string]$Description = "Carnavacs Turnstile Management API",
    [string]$InstallPath = "C:\Services\CarnavalAPI",
    [int]$Port = 5000,
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warn { Write-Host $args -ForegroundColor Yellow }
function Write-Error { param([string]$Message) Write-Host $Message -ForegroundColor Red }

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Error "ERROR: This script must be run as Administrator"
    exit 1
}

# Uninstall service
if ($Uninstall) {
    Write-Info "🗑️  Uninstalling service..."
    
    $service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($service) {
        if ($service.Status -eq "Running") {
            Write-Info "Stopping service..."
            Stop-Service -Name $ServiceName -Force
        }
        
        Write-Info "Removing service..."
        sc.exe delete $ServiceName
        
        Write-Success "✅ Service uninstalled"
    } else {
        Write-Warn "Service '$ServiceName' not found"
    }
    exit 0
}

# Install service
Write-Info "📦 Installing Carnavacs API as Windows Service"
Write-Info "=============================================="
Write-Info ""

# Get script directory (where the .csproj is)
$ScriptDir = Split-Path -Parent $PSScriptRoot
$ProjectFile = Join-Path $ScriptDir "Carnavacs.Api.csproj"

if (-not (Test-Path $ProjectFile)) {
    Write-Error "ERROR: Project file not found at $ProjectFile"
    exit 1
}

# Build the application
Write-Info "📦 Building application..."
try {
    $buildOutput = Join-Path $ScriptDir "bin\Release\net9.0-windows\publish"
    
    dotnet publish $ProjectFile `
        --configuration Release `
        --output $buildOutput `
        --self-contained false `
        --verbosity minimal
    
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed"
    }
    
    Write-Success "✅ Build successful"
} catch {
    Write-Error "ERROR: Build failed - $_"
    exit 1
}

# Copy files to install directory
Write-Info "📤 Installing to $InstallPath..."
try {
    if (-not (Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    }
    
    # Copy all files
    Copy-Item -Path "$buildOutput\*" -Destination $InstallPath -Recurse -Force
    
    # Create logs directory
    $logsPath = Join-Path $InstallPath "logs"
    if (-not (Test-Path $logsPath)) {
        New-Item -ItemType Directory -Path $logsPath -Force | Out-Null
    }
    
    Write-Success "✅ Files installed"
} catch {
    Write-Error "ERROR: Installation failed - $_"
    exit 1
}

# Update appsettings for service
Write-Info "⚙️  Configuring service settings..."
try {
    $appsettingsPath = Join-Path $InstallPath "appsettings.json"
    if (Test-Path $appsettingsPath) {
        $appsettings = Get-Content $appsettingsPath | ConvertFrom-Json
        
        # Update log path to use Windows format
        if ($appsettings.Serilog.WriteTo) {
            foreach ($sink in $appsettings.Serilog.WriteTo) {
                if ($sink.Name -eq "File" -and $sink.Args.path) {
                    $sink.Args.path = "$logsPath\log-.txt"
                }
            }
        }
        
        $appsettings | ConvertTo-Json -Depth 10 | Set-Content $appsettingsPath
        Write-Success "✅ Configuration updated"
    }
} catch {
    Write-Warn "Could not update appsettings: $_"
}

# Create Windows Service
Write-Info "🔧 Creating Windows Service..."
try {
    # Check if service already exists
    $existingService = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($existingService) {
        Write-Info "Service already exists, updating..."
        Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
        sc.exe delete $ServiceName
        Start-Sleep -Seconds 2
    }
    
    # Create service using sc.exe
    $exePath = Join-Path $InstallPath "Carnavacs.Api.exe"
    
    sc.exe create $ServiceName `
        binPath= "`"$exePath`"" `
        start= auto `
        DisplayName= $DisplayName
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create service"
    }
    
    # Set description
    sc.exe description $ServiceName $Description
    
    # Configure service recovery options (restart on failure)
    sc.exe failure $ServiceName reset= 86400 actions= restart/60000/restart/60000/restart/60000
    
    Write-Success "✅ Service created"
} catch {
    Write-Error "ERROR: Service creation failed - $_"
    exit 1
}

# Configure firewall
Write-Info "🔥 Configuring firewall..."
try {
    $ruleName = "Carnavacs API Service - Port $Port"
    $existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
    
    if (-not $existingRule) {
        New-NetFirewallRule -DisplayName $ruleName `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort $Port `
            -Action Allow `
            -Profile Domain,Private,Public
        
        Write-Success "✅ Firewall rule created for port $Port"
    } else {
        Write-Info "Firewall rule already exists"
    }
} catch {
    Write-Warn "Could not configure firewall: $_"
}

# Start the service
Write-Info "▶️  Starting service..."
try {
    Start-Service -Name $ServiceName
    Start-Sleep -Seconds 3
    
    $service = Get-Service -Name $ServiceName
    if ($service.Status -eq "Running") {
        Write-Success "✅ Service started successfully"
    } else {
        Write-Warn "⚠️  Service state: $($service.Status)"
    }
} catch {
    Write-Error "ERROR: Could not start service - $_"
    Write-Info "Check Event Viewer for details"
    exit 1
}

# Summary
Write-Info "`n✅ Installation Complete!"
Write-Info "========================"
Write-Info "Service Name: $ServiceName"
Write-Info "Install Path: $InstallPath"
Write-Info "Port: $Port"
Write-Info "URL: http://localhost:$Port"
Write-Info ""
Write-Info "Useful commands:"
Write-Info "  Start:   Start-Service $ServiceName"
Write-Info "  Stop:    Stop-Service $ServiceName"
Write-Info "  Restart: Restart-Service $ServiceName"
Write-Info "  Status:  Get-Service $ServiceName"
Write-Info "  Logs:    Get-Content '$logsPath\log-*.txt' -Tail 50 -Wait"
Write-Info "  Remove:  .\install-as-service.ps1 -Uninstall"
Write-Info ""
Write-Info "Check Event Viewer > Windows Logs > Application for service events"
