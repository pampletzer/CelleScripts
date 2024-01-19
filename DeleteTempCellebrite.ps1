# Written by Paul Ampletzer @ paul.ampletzer@gmail.com

#TODO: catching error if user has no matching folder

#Getting admin rights
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    
    #List of all users
    $users = Get-ChildItem C:\Users
    $NameToFind = "Cellebrite"

    #checking every user
    foreach ($user in $users){
        #building the temp path for the current user of foreach
        $folder = "$($user.fullname)\AppData\Local\Temp\"
        #searching for Folders containing $NameToFind
        $FoundFolders = Get-ChildItem $folder -Recurse | Where-Object { $_.PSIsContainer -and $_.Name.Contains($NameToFind)}
        echo $FoundFolders
        #going through every $NameToFind Folder 
        ForEach ($Dir in $FoundFolders) {
            If (Test-Path $folder$Dir) {
                # Folder exist, delete it!
                Remove-Item -Path $folder$Dir -Recurse -Force
                Write-host "Folder Deleted at '$folder$Dir'!" -f Green
            }
            Else {
                Write-host "Folder '$folder$Dir' does not exists!" -f Red
            }
            
        }
    }
    #If running as Admin you wont get to see the output without pause, so now you have to be interaktiv. Remove if not wanted.
    Pause 
}
else {
    Start-Process -FilePath "powershell" -ArgumentList "$('-File ""')$(Get-Location)$('\')$($MyInvocation.MyCommand.Name)$('""')" -Verb runAs
}



