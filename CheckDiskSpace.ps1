$VarSpace = $(Get-WmiObject -Class win32_logicaldisk | Where-Object -Property Name -eq C:).FreeSpace/1GB

if ($VarSpace -le 10){ 
    echo "Speicher läuft voll"
} else {
    echo "Speicher passt. Noch " $VarSpace  "GB frei"
}
