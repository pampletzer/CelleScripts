# Userprompt
$timestamp = Read-Host "Zeitstempel:"

if ($timestamp.Length -eq 13) {
	$timestamp = [int64]$timestamp / 1000
	Write-Host "Android Timestamp"
} elseif ($timestamp.Length -eq 10) {
	Write-Host "Unix Timestamp"
} else {
	Write-Host "Kein Gülter Timestamp"
}


try {
	$date = [DateTimeOffset]::FromUnixTimeSeconds([int64]$timestamp).LocalDateTime
	write-Host "$date"
} catch {
	Write-Host "Kein gültiger Timestamp"
}

Read-Host -Prompt "exit"