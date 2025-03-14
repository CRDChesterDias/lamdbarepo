# Initialize PCOMM COM Object
$pcSession = New-Object -ComObject PCOMM.autECLSession
$pcSession.SetConnectionByName("A")  # Adjust session name (e.g., A, B, etc.)

# Ensure the session is ready
$pcSession.autECLOIA.WaitForAppAvailable()
$pcSession.autECLOIA.WaitForInputReady()

Write-Host "Connected to IBM PCOMM session"

# Define login credentials
$username = "your_username"
$password = "your_password"

# Move cursor to the username field and enter username
$pcSession.autECLPS.SetCursorPos(5, 20)  # Adjust based on screen layout
$pcSession.autECLPS.SendKeys($username)

# Move cursor to the password field and enter password
$pcSession.autECLPS.SetCursorPos(6, 20)  # Adjust row/column as needed
$pcSession.autECLPS.SendKeys($password)

# Press Enter to submit login
$pcSession.autECLPS.SendKeys("[enter]")

Start-Sleep -Seconds 2  # Wait for login to complete

# Example: Navigate to a menu option
$pcSession.autECLPS.SendKeys("1")  # Select option 1
$pcSession.autECLPS.SendKeys("[enter]")

Write-Host "Operation performed successfully!"
