# Neom Asistan - Otomatik baslatma kurulumu (Task Scheduler)
# Oturum acildiginda pythonw.exe ile gizli sekilde baslatir.

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$MainPy      = Join-Path $ProjectRoot "src\main.py"
$TaskName    = "NeomAsistan"

if (-not (Test-Path $MainPy)) {
    Write-Error "main.py bulunamadi: $MainPy"
    exit 1
}

$pythonw = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $pythonw) {
    Write-Error "pythonw.exe bulunamadi. Python kurulu mu? (Python.org'dan yukleyip PATH'e ekleyin)"
    exit 1
}

Write-Host "Python: $pythonw"
Write-Host "Proje:  $ProjectRoot"

$Action = New-ScheduledTaskAction `
    -Execute $pythonw `
    -Argument "`"$MainPy`"" `
    -WorkingDirectory $ProjectRoot

$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Neom sesli asistani, oturum acilinca gizli baslatir." `
    -Force | Out-Null

Write-Host ""
Write-Host "Kurulum tamam. Bir sonraki oturum acilisinda Neom otomatik calismaya baslayacak."
Write-Host "Hemen test etmek icin: Start-ScheduledTask -TaskName $TaskName"
Write-Host "Log dosyasi: $env:LOCALAPPDATA\NeomPro\neom.log"
