from transactions.models import BankAccount, TransactionLabel

halifaxCredit = BankAccount()
halifaxCredit.AccountHumanName = 'Halifax Credit'
halifaxCredit.AccountType = 'CreditCard'
halifaxCredit.AccountNumber = ''
halifaxCredit.SortCode = ''
halifaxCredit.IsActive = True

halifaxCredit.ColumnDate = "datetime.strptime(row['Date'], '%d/%m/%y')"
halifaxCredit.ColumnDescription = "row['Description']"
halifaxCredit.ColumnAmount = "-float(row['Amount'])"
halifaxCredit.ColumnCurrentBalance = "None"
halifaxCredit.OtherDate1Name = "Date entered"
halifaxCredit.ColumnOtherDate1 = "datetime.strptime(row['Date entered'], '%d/%m/%y')"
halifaxCredit.OtherString1Name = "Reference"
halifaxCredit.ColumnOtherString1 = "row['Reference']"

halifaxCredit.save()

natwestCurrent = BankAccount()
natwestCurrent.AccountHumanName = 'Natwest Current'
natwestCurrent.AccountType = 'CurrentAccount'
natwestCurrent.AccountNumber = ''
natwestCurrent.SortCode = ''
natwestCurrent.IsActive = True

natwestCurrent.ColumnDate = "datetime.strptime(row['Date'], '%d %b %Y')"
natwestCurrent.ColumnDescription = "row['Description']"
natwestCurrent.ColumnAmount = "float(row['Value'])"
natwestCurrent.ColumnCurrentBalance = "float(row['Balance'])"
natwestCurrent.OtherDate1Name = None
natwestCurrent.ColumnOtherDate1 = "None"
natwestCurrent.OtherString1Name = "Type"
natwestCurrent.ColumnOtherString1 = "row['Type']"

natwestCurrent.save()

TransactionLabel.create('Supermarket').save()
TransactionLabel.create('Drinks').save()
TransactionLabel.create('Food').save()
TransactionLabel.create('Travel').save()
TransactionLabel.create('Coffee').save()