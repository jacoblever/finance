from transactions.models import BankAccount, TransactionLabel, BankAccountTemplate


def get_built_in_item(cls, id_):
    try:
        return cls.objects.get(pk=id_)
    except cls.DoesNotExist:
        new_item = cls()
        new_item.id = id_
        return new_item

manual_template = get_built_in_item(BankAccountTemplate, -1)
manual_template.name = "Manual"
manual_template.is_built_in = True
manual_template.get_date = "datetime.strptime(row['Date'], '%d %b %Y')"
manual_template.get_description = "row['Description']"
manual_template.get_amount = "float(row['Amount'])"
manual_template.get_current_balance = "None"
manual_template.custom_date_1_name = None
manual_template.get_custom_date_1 = "None"
manual_template.custom_text_1_name = None
manual_template.get_custom_text_1 = "None"
manual_template.save()

halifax = get_built_in_item(BankAccountTemplate, -2)
halifax.name = "Halifax"
halifax.is_built_in = True
halifax.get_date = "datetime.strptime(row['Date'], '%d/%m/%y')"
halifax.get_description = "row['Description']"
halifax.get_amount = "-float(row['Amount'])"
halifax.get_current_balance = "None"
halifax.custom_date_1_name = "Date entered"
halifax.get_custom_date_1 = "datetime.strptime(row['Date entered'], '%d/%m/%y')"
halifax.custom_text_1_name = "Reference"
halifax.get_custom_text_1 = "row['Reference']"
halifax.save()

natwest = get_built_in_item(BankAccountTemplate, -3)
natwest.name = "Natwest"
natwest.is_built_in = True
natwest.get_date = "datetime.strptime(row['Date'], '%d %b %Y')"
natwest.get_description = "row['Description']"
natwest.get_amount = "float(row['Value'])"
natwest.get_current_balance = "float(row['Balance'])"
natwest.custom_date_1_name = None
natwest.get_custom_date_1 = "None"
natwest.custom_text_1_name = "Type"
natwest.get_custom_text_1 = "row['Type']"
natwest.save()

nationwide = get_built_in_item(BankAccountTemplate, -4)
nationwide.name = "Nationwide"
nationwide.is_built_in = True
nationwide.get_date = "datetime.strptime(row['Date'], '%d %b %Y')"
nationwide.get_description = "row['Description']"
nationwide.get_amount = "(float(row['Paid in'].replace('£','')) if row['Paid in']!='' else 0) - (float(row['Paid out'].replace('£','')) if row['Paid out']!='' else 0)"
nationwide.get_current_balance = "float(row['Balance'].replace('£',''))"
nationwide.custom_date_1_name = None
nationwide.get_custom_date_1 = "None"
nationwide.custom_text_1_name = "Transaction type"
nationwide.get_custom_text_1 = "row['Transaction type']"
nationwide.save()


manual = get_built_in_item(BankAccount, -1)
manual.name = 'Manual'
manual.account_type = 'CurrentAccount'
manual.more_details = ''
manual.is_active = True
manual.bank_account_template = manual_template
manual.save()


transfer = get_built_in_item(TransactionLabel, -1)
transfer.name = 'Internal Transfer'
transfer.save()

