# Initial Windows Server Setup Script
# This script installs all prerequisites for the Carnavacs API

param(
    [switch]$SkipDotNet,
    [switch]$SkipIIS
)

$ErrorActionPreference = "Stop"

function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warn { Write-Host $args -ForegroundColor Yellow }
function Write-Error { param([string]$Message) Write-Host $Message -ForegroundColor Red }

Write-Info "🔧 Carnavacs API - Windows Server Setup"
Write-Info "========================================"
Write-Info ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Error "ERROR: This script must be run as Administrator"
    Write-Warn "Right-click PowerShell and select 'Run as Administrator'"
    exit 1
}

# Step 1: Install IIS and ASP.NET Core Hosting Bundle
if (-not $SkipIIS) {
    Write-Info "📦 Installing IIS..."
    try {
        # Check if IIS is already installed
        $iisFeature = Get-WindowsFeature -Name Web-Server
        
        if ($iisFeature.InstallState -eq "Installed") {
            Write-Success "✅ IIS already installed"
        } else {
            Write-Info "Installing IIS and required features..."
            
            Install-WindowsFeature -Name Web-Server `
                -IncludeManagementTools `
                -IncludeAllSubFeature
            
            Write-Success "✅ IIS installed"
        }
        
        # Install required IIS features for ASP.NET Core
        $features = @(
            "Web-Http-Redirect",
            "Web-Custom-Logging",
            "Web-Log-Libraries",
            "Web-Request-Monitor",
            "Web-Http-Tracing",
            "Web-Stat-Compression",
            "Web-Dyn-Compression",
            "Web-Filtering",
            "Web-Windows-Auth",
            "Web-AppInit"
        )
        
        foreach ($feature in $features) {
            $installed = Get-WindowsFeature -Name $feature
            if ($installed.InstallState -ne "Installed") {
                Write-Info "Installing $feature..."
                Install-WindowsFeature -Name $feature
            }
        }
        
    } catch {
        Write-Error "ERROR: IIS installation failed - $_"
        exit 1
    }
} else {
    Write-Warn "Skipping IIS installation"
}

# Step 2: Install .NET 9.0 Runtime and Hosting Bundle
if (-not $SkipDotNet) {
    Write-Info "`n📦 Checking .NET 9.0..."
    try {
        # Check if dotnet is installed
        $dotnetPath = Get-Command dotnet -ErrorAction SilentlyContinue
        
        if ($dotnetPath) {
            $version = dotnet --version
            Write-Info "Found .NET SDK: $version"
            
            # Check for ASP.NET Core runtime
            $runtimes = dotnet --list-runtimes
            $hasAspNetCore9 = $runtimes | Select-String "Microsoft.AspNetCore.App 9."
            
            if ($hasAspNetCore9) {
                Write-Success "✅ .NET 9.0 ASP.NET Core Runtime found"
            } else {
                Write-Warn "⚠️  .NET 9.0 ASP.NET Core Runtime not found"
                Write-Info "Please install the ASP.NET Core 9.0 Hosting Bundle:"
                Write-Info "https://dotnet.microsoft.com/download/dotnet/9.0"
                Write-Info ""
                Write-Info "Download: ASP.NET Core Runtime 9.0.x - Windows Hosting Bundle Installer"
            }
        } else {
            Write-Warn "⚠️  .NET SDK not found"
            Write-Info ""
            Write-Info "Please install .NET 9.0 SDK or Runtime:"
            Write-Info "https://dotnet.microsoft.com/download/dotnet/9.0"
            Write-Info ""
            Write-Info "For production servers, download:"
            Write-Info "  - ASP.NET Core Runtime 9.0.x - Windows Hosting Bundle Installer"
            Write-Info ""
            Write-Info "For development machines, download:"
            Write-Info "  - .NET 9.0 SDK"
            Write-Info ""
            Write-Info "After installation, restart this script."
        }
    } catch {
        Write-Warn "Could not check .NET installation: $_"
    }
} else {
    Write-Warn "Skipping .NET check"
}

# Step 3: Configure Windows Firewall
Write-Info "`n🔥 Configuring Windows Firewall..."
try {
    # Check if firewall rule exists
    $ruleName = "Carnavacs API - HTTP"
    $existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
    
    if ($existingRule) {
        Write-Info "Firewall rule already exists"
    } else {
        Write-Info "Creating firewall rule for HTTP (port 80)..."
        New-NetFirewallRule -DisplayName $ruleName `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort 80 `
            -Action Allow `
            -Profile Domain,Private,Public
        
        Write-Success "✅ Firewall rule created"
    }
    
    # Optional: HTTPS rule
    $httpsRuleName = "Carnavacs API - HTTPS"
    $existingHttpsRule = Get-NetFirewallRule -DisplayName $httpsRuleName -ErrorAction SilentlyContinue
    
    if (-not $existingHttpsRule) {
        Write-Info "Creating firewall rule for HTTPS (port 443)..."
        New-NetFirewallRule -DisplayName $httpsRuleName `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort 443 `
            -Action Allow `
            -Profile Domain,Private,Public
        
        Write-Success "✅ HTTPS firewall rule created"
    }
} catch {
    Write-Warn "Could not configure firewall: $_"
    Write-Info "You may need to configure firewall rules manually"
}

# Step 4: Create deployment directory
Write-Info "`n📁 Creating deployment directory..."
try {
    $deployPath = "C:\inetpub\wwwroot\CarnavalAPI"
    if (-not (Test-Path $deployPath)) {
        New-Item -ItemType Directory -Path $deployPath -Force | Out-Null
        Write-Success "✅ Created: $deployPath"
    } else {
        Write-Info "Directory already exists: $deployPath"
    }
    
    # Create logs directory
    $logsPath = Join-Path $deployPath "logs"
    if (-not (Test-Path $logsPath)) {
        New-Item -ItemType Directory -Path $logsPath -Force | Out-Null
        Write-Success "✅ Created logs directory"
    }
} catch {
    Write-Warn "Could not create deployment directory: $_"
}

# Summary
Write-Info "`n✅ Setup Complete!"
Write-Info "=================="
Write-Info ""
Write-Info "Next steps:"
Write-Info "1. Copy appsettings.json.sample to appsettings.json and configure:"
Write-Info "   - SQL Server connection string"
Write-Info "   - API keys"
Write-Info "   - Log paths (use Windows paths like C:\logs)"
Write-Info ""
Write-Info "2. Deploy the application:"
Write-Info "   .\deploy\deploy.ps1"
Write-Info ""
Write-Info "3. Configure your SQL Server connection"
Write-Info "4. Test the API: http://localhost/swagger"
Write-Info ""
Write-Warn "⚠️  Remember to restart IIS after installing .NET Hosting Bundle:"
Write-Warn "   Restart-Service W3SVC"
