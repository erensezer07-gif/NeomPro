# Neom Asistan - Otomatik baslatmayi kaldir
$TaskName = "NeomAsistan"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Otomatik baslatma kaldirildi."
} else {
    Write-Host "Zaten kurulu degil ($TaskName)."
}
