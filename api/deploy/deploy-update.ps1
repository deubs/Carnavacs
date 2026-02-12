# Carnavacs API Update Script
# Pulls latest code, publishes, and restarts IIS
# Run on 192.168.40.100 as Administrator

param(
    [string]$RepoPath = "C:\src\Carnavacs",
    [string]$DeployPath = "C:\sites\api.carnavaldelpais.com.ar",
    [string]$AppPoolName = "CarnavalAPIPool",
    [string]$Configuration = "Release"
)

$ErrorActionPreference = "Stop"
Import-Module WebAdministration

# Pull latest
Write-Host "Pulling latest changes..."
Set-Location $RepoPath
git pull origin main
if ($LASTEXITCODE -ne 0) { throw "git pull failed" }

# Publish
$ProjectFile = Join-Path $RepoPath "src\api\Carnavacs.Api.csproj"
$PublishDir = Join-Path $RepoPath "publish"

Write-Host "Publishing..."
dotnet publish $ProjectFile --configuration $Configuration --output $PublishDir --verbosity minimal
if ($LASTEXITCODE -ne 0) { throw "dotnet publish failed" }

# Stop AppPool
Write-Host "Stopping AppPool..."
if ((Get-WebAppPoolState -Name $AppPoolName).Value -eq "Started") {
    Stop-WebAppPool -Name $AppPoolName
    Start-Sleep -Seconds 3
}

# Copy files
Write-Host "Copying files to $DeployPath..."
Copy-Item -Path "$PublishDir\*" -Destination $DeployPath -Recurse -Force

# Start AppPool
Write-Host "Starting AppPool..."
Start-WebAppPool -Name $AppPoolName
Start-Sleep -Seconds 2

# Verify
$state = (Get-WebAppPoolState -Name $AppPoolName).Value
if ($state -eq "Started") {
    Write-Host "OK: $AppPoolName is $state" -ForegroundColor Green
} else {
    Write-Host "FAIL: $AppPoolName is $state" -ForegroundColor Red
    exit 1
}
