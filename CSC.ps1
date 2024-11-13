### CSC Chat Schönheits Chirurg


# Displays a message to the user informing them that this tool creates a second version of their report,
# where certain file system information is automatically hidden.
Write-Host -NoNewLine ' Lieber Kollege / Liebe Kollegin,
mit dem Ausführen des CSC - Chat Schönheits Chirurg Tools erzeugst du eine zweite Version deines Reports, bei der automatisiert die Dateisysteminformationen ausgeblendet werden.
Es ist wichtig, die Vollständigkeit selbstständig zu überprüfen. Ungeachtet dessen verkauft der Nutzer hiermit sein Erstgeborenes und 10kg Koks.
Der Original Bericht sollte der Vollständigkeithalber aufbehalten werden.

Press' ([char]9992) 'to continue...';

# Waits for a key press to continue
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');

# Defines the names of the original and the new HTML files
$html = "Report.html"
$htmlNew = "Print_Report.html"
# Initializes the counter for the progress bar
$x = 1

# Reads the content of the original HTML file and set an break, so we can add a new line in the next step
(Get-Content $html) -replace '\<style type\=\"text\/css\" media\=\"all\"\>', '<style type="text/css" media="all">
 ' | Set-Content $htmlNew -Encoding utf8

# Gets the total number of lines in the new HTML file
$htmllines = (Get-Content $htmlNew).length

# Processes each line of the new HTML file
(Get-Content $htmlNew) |
    Foreach-Object {

        # Calculates the current progress as a percentage
        $perc=[math]::round($x/$htmllines*100)

        # Displays the progress in the terminal
        Write-progress -id 1 -percent $perc -activity "Looking up $($_)"

        # Increments the counter for the next line
        $x++

        # send the current line to output
        $_

        # Checks if the line contains the CSS Style Tag
        if ($_ -match '\<style type\=\"text\/css\" media\=\"all\"\>') {

            # Adds CSS code after the found line to hide certain HTML elements
            ".stack .stack span {
            display: none;
            }"
        }
    } | Set-Content $htmlNew -Encoding utf8

# Replaces the closing </body> tag at the end of the HTML file with a new, formatted HTML content
#(Get-Content mytest.html).Replace('\<\/body\>', '<b>hier kommt die Nachricht!</b></body>') | Set-Content mytest.html
(Get-Content $htmlNew) -replace '\<\/body\>', '<div style="text-align: center;color: #1eff4e;box-shadow: 0 0 10px #1eff4e, 0 0 30px #1eff4e, inset 0 0 10px #1eff4e,inset 0 0 30px #1eff4e;border-radius:  10px;padding:  20px 50 px;border: 4px solid #fff;background: black;margin: 28px; padding-bottom: 20px; padding-top: 20px;"><h2 style="text-align: center;"><b>Es handelt sich hierbei um eine automatisiert gek&uuml;rzte Version. <br /> Chatinhalte sollten unver&auml;ndert sein.</b></h2> <br /> <h3 style="text-align: center;">ggf. den Originalen Export konsultieren!</h3> <br /> <span>created by Ampletzer</span></div></body>' | Set-Content $htmlNew -Encoding utf8

# Adds empty lines for better readability in the terminal
Write-Host "
"
Write-Host "
"
Write-Host "
"

# Displays a completion message indicating the process finished without errors
Write-Host  '

Ohne Fehler abgeschlossen. Press any Key to close.
';

# Waits for any key press to close the script
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');