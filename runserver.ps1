param (
	[string] $Database,
	[switch] $Test,
	[switch] $Quick
)
$DEFAULT_DATABASE_PATH="./data/default_db.sqlite3"
$TEST_DATABASE_PATH="./data/test_db.sqlite3"
if ($Database -eq "") {
	$database_path=$DEFAULT_DATABASE_PATH
} else {
	$database_path = $Database
}
if ($Test) {
	$database_path = $TEST_DATABASE_PATH
}

if ( Test-Path $database_path ) {
    Write-Host ("Using database {0}" -f $database_path)
} else {
	Write-Host "Database $database_path does not exist."
	$answer = Read-Host "Would you like to install a database at this location? (yes/no) "
	while (@("yes","y","no","n") -notcontains $answer) {
		$answer = Read-Host "Please answer yes or no."
	}
	if($answer.StartsWith("n")) {
		Write-Host "Cancelled"
		exit
	}
    
	if ($database_path -eq $DEFAULT_DATABASE_PATH) {
        # Ensure data directory exists
        md -Force data
        .\install_db.ps1 -Path $DEFAULT_DATABASE_PATH
    } elseif ($database_path -eq $TEST_DATABASE_PATH) {
    
        # Ensure data directory exists
        md -Force data
        .\install_db.ps1 -Path $TEST_DATABASE_PATH -Test -AddSuperUser
    } else {
        .\install_db.ps1 -Path $database_path
    }
}

$env:FINANCE_DATABASE_NAME = $database_path
if (-not $Quick) {
    python3 manage.py ensure_setup
}

python3 manage.py runserver