param (
    [Parameter(Mandatory=$true)]
	[string] $Path,
	[switch] $AddSuperUser,
	[switch] $Test
)

if (Test-Path $Path) {
	Write-Host "Database already exists!"
	$answer = Read-Host "This will permanently delete all data in $Path and CANNOT be undone. (yes/no) "
	while (@("yes","y","no","n") -notcontains $answer) {
		$answer = Read-Host "Please answer yes or no."
	}
	if ($answer.StartsWith("n")) {
		exit 0
	}
}

echo "Installing database at $Path..."
$env:FINANCE_DATABASE_NAME = $Path
rm -Force $Path -ErrorAction Ignore
rm -Force ./transactions/migrations/0001_initial.py -ErrorAction Ignore
python manage.py makemigrations
python manage.py migrate
python manage.py ensure_setup

if($AddSuperUser) {
	python manage.py createsuperuser --username admin --email admin@localhost
}

if($Test) {
	python manage.py install_test_data
}

echo "Database installed at $Path"
