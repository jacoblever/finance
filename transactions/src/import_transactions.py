import csv
from io import TextIOWrapper
from transactions.models import BankAccount, Transaction, TransactionLabel, BankAccountTemplate
from datetime import datetime
from decimal import Decimal


def import_transactions(form, actually_import):
    file = TextIOWrapper(form.get_file().file, encoding='ISO-8859-1')
    import_transactions_core(file, form.get_account(), actually_import)


def import_transactions_core(file, account, actually_import):
    transaction_id_col = 'TransactionId'

    reader = csv.DictReader(file)
    #for row in reader:
    #    print("row: " + row)
    duplicates = Transaction.objects.none()
    duplicates_so_far = list(Transaction.objects.none())
    labels = TransactionLabel.objects.all()
    account = BankAccount.objects.get(pk=account) if account != '' else None
    now = datetime.now()
    problems = []

    existing_count = 0
    count = 0
    for row in reader:
        count += 1
        transaction = Transaction()
        existing_transaction = False
        if transaction_id_col in row and row[transaction_id_col] != "":
            id_ = int(row[transaction_id_col])
            transaction = Transaction.objects.get(pk=id_)
            new_temp = Transaction()
            populate_bank_transaction_info(new_temp, row, get_reimport_account_template())
            if transaction.bank_account.id != int(row['AccountId']):
                problems.append(str(id_) + ": Account id changed " + str(transaction.bank_account.id) + " != " + row['AccountId'])
            for problem in check_bank_transaction_info_consistency(transaction, new_temp):
                problems.append(str(id_) + ": " + problem)
            existing_transaction = True
            existing_count += 1
        else:
            transaction.bank_account = account
            transaction.date_imported = now
            if account == None:
                problems.append("Could not parse transaction: Please select an account")
            else:
                try:
                    populate_bank_transaction_info(transaction, row, account.bank_account_template)
                except Exception as e:
                    problems.append("Could not parse transaction: '" + str(e) + "'")

        populate_meta_transaction_info(transaction, row, labels)

        if actually_import:
            if len(problems) > 0:
                file = "\n".join(["- " + x for x in problems])
                raise Exception("Cannot save if there are problems:\n" + file)
            transaction.save()
        else:
            if not existing_transaction:
                duplicates = duplicates | Transaction.objects.all().filter(
                    date = transaction.date,
                    description = transaction.description,
                    amount = transaction.amount,
                    current_balance = transaction.current_balance,
                    custom_date_1 = transaction.custom_date_1,
                    custom_text_1 = transaction.custom_text_1,
                    )
            if count % 50 == 0:
                duplicates_so_far = duplicates_so_far + list(duplicates)
                duplicates = Transaction.objects.none()

    duplicates_so_far = duplicates_so_far + list(duplicates)
    return count, list(duplicates_so_far), existing_count, problems


def check_bank_transaction_info_consistency(t1, t2):
    problems = []
    test(problems, t1, t2, lambda x: x.date.strftime('%m/%d/%Y'))
    test(problems, t1, t2, lambda x: x.description)
    test(problems, t1, t2, lambda x: x.amount)
    test(problems, t1, t2, lambda x: x.current_balance)
    test(problems, t1, t2, lambda x: None if x.custom_date_1 == None else x.custom_date_1.strftime('%m/%d/%Y'))
    test(problems, t1, t2, lambda x: x.custom_text_1)
    return problems


def test(problems, t1, t2, lam):
    if lam(t1) != lam(t2):
        problems.append("'" + str(lam(t1))  + "' != '" + str(lam(t2) + "'"))


def get_reimport_account_template():
    template = BankAccountTemplate()

    template.get_date = "datetime.strptime(row['Date'], '%d %b %Y')"
    template.get_description = "row['Description']"
    template.get_amount = "Decimal(row['Amount'])"
    template.get_current_balance = "None if row['CurrentBalance'] == '' else Decimal(row['CurrentBalance'])"
    template.get_custom_date_1 = "None if row['CustomDate1'] == '' else datetime.strptime(row['CustomDate1'], '%d %b %Y')"
    template.get_custom_text_1 = "row['CustomText1']"

    return template


############################################################
# Note: Do not remove the row parameter, it must exist in
# the scope the getters are run
############################################################
def populate_bank_transaction_info(transaction, row, template):
    transaction.date = eval(template.get_date)
    transaction.description = eval(template.get_description)
    transaction.amount = eval(template.get_amount)
    transaction.current_balance = eval(template.get_current_balance)\
        if template.get_current_balance is not None else None
    transaction.custom_date_1 = eval(template.get_custom_date_1)\
        if template.get_custom_date_1 is not None else None
    transaction.custom_text_1 = eval(template.get_custom_text_1)\
        if template.get_custom_text_1 is not None else None


def populate_meta_transaction_info(transaction, row, labels):
    LABEL_COLUMN = 'Label'
    NOTES_COLUMN = 'Notes'

    transaction.notes = ''

    if LABEL_COLUMN in row:
        label_text = row[LABEL_COLUMN]
        if(label_text != None and label_text != ''):
            label = next((x for x in labels if x.name == label_text), None)
            if(label != None):
                transaction.transaction_label = label
            else:
                transaction.notes = label_text

    if NOTES_COLUMN in row:
        notes = row[NOTES_COLUMN]
        if(notes != None and notes != ''):
            if(transaction.notes != None and transaction.notes != ''):
                transaction.notes = transaction.notes + ', ' + notes
            else:
                transaction.notes = notes

