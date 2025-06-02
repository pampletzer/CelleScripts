

# Load the necessary .NET assembly for Windows Forms to enable GUI elements.
Add-Type -AssemblyName System.Windows.Forms

# Create a new OpenFileDialog object, which will be used to display the file selection dialog.
$OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog

# Set the initial directory for the dialog. This makes it more user-friendly by starting in a common location.
# [Environment]::GetFolderPath("MyDocuments") points to the user's "Documents" folder.
$OpenFileDialog.InitialDirectory = [Environment]::GetFolderPath("MyDocuments")

# Set the title of the file selection dialog window. This provides clear instructions to the user.
$OpenFileDialog.Title = "Please select the source 'test.txt' file"

# Define a filter for file types. This helps the user find the correct file by showing only relevant extensions.
# Format: "Description (*.extension)|*.extension)|All files (*.*)|*.*"
$OpenFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*"

# Set MultiSelect to $false to ensure the user can only select a single file.
$OpenFileDialog.MultiSelect = $false

# Show the dialog to the user and capture the result.
# The script will pause here until the user makes a selection (OK or Cancel).
$DialogResult = $OpenFileDialog.ShowDialog()

# Check if the user clicked "OK" (meaning a file was selected).
if ($DialogResult -eq [System.Windows.Forms.DialogResult]::OK) {
    # If a file was selected, get its full path and store it in $SourceFilePath.
    $SourceFilePath = $OpenFileDialog.FileName
    #Write-Host "You selected the file: $SourceFilePath"
} else {
    # If the user cancelled the dialog, display a message and exit the script.
    Write-Host "File selection cancelled. Exiting script."
    # Dispose of the dialog object to release system resources.
    $OpenFileDialog.Dispose()
    exit
}

# Dispose of the OpenFileDialog object to free up system resources after use.
$OpenFileDialog.Dispose()

# Get the directory part of the selected source file path.
$OutputDirectory = Split-Path -Path $SourceFilePath -Parent


# Gets the file into an array
$array = Get-Content -Path $SourceFilePath # Now uses the selected file path

# Gets the file into an array
#$array = Get-Content -Path @("TBK_LKA_NI_HASHDB_2025-05-26_14-36-22.txt")

# Gets the total number of lines in the Hashfile file
$hashlines = $array.Length


# This variable will collect all the md5 hashes.
$mdfive = @()

# This variable will collect all the SHA hashes.
$SHA = @()

# initiate $x
$x = 0

# going through the array line by line
foreach($item in $array) {

	# Calculates the current progress as a percentage
	$perc=[math]::round($x/$hashlines*100)

	# Displays the progress in the terminal
    Write-progress -id 1 -PercentComplete $perc -activity "Looking up $($_)"

	# Increments the counter for the next line
	$x++

	# send the current line to output
	$_

	# gets the 4 Item in the Hashfile sepparated by tabs
	$mdfive += $item.Split("`t")[4] #| Out-Host

	# gets the 8 Item in the Hashfile sepparated by tabs
	$SHA += $item.Split("`t")[8] #| Out-Host



}

# sets the output folder / name
$OutputFilePathmd5 = Join-Path -Path $OutputDirectory -ChildPath "md5.txt"
$OutputFilePathsha = Join-Path -Path $OutputDirectory -ChildPath "sha.txt"

#$OutputFilePathmd5 = "md5.txt"
#$OutputFilePathsha = "sha.txt"

# Write the collected strings to a text file.
# Each element of the array will automatically be written to a new line.
$mdfive | Set-Content -Path $OutputFilePathmd5
$SHA | Set-Content -Path $OutputFilePathsha

#Press Enter!
Read-Host -Prompt "Script finished. Press any key (except 'Q') to recall your funniest childhood memory, then hit Enter"