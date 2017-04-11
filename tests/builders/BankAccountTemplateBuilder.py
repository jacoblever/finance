from transactions.models import BankAccountTemplate


class BankAccountTemplateBuilder:

    def __init__(self):
        self.template = BankAccountTemplate()
        self.template.name = "Test bank account template"
        self.template.is_built_in = False
        self.template.get_date = "datetime.strptime(row['Date'], '%d/%m/%y')"
        self.template.get_description = "row['Description']"
        self.template.get_amount = "float(row['Amount'])"
        self.template.get_current_balance = "float(row['CurrentBalance'])"
        self.template.custom_date_1_name = "Custom Date 1"
        self.template.get_custom_date_1 = "datetime.strptime(row['CustomDate1'], '%d/%m/%y')"
        self.template.custom_text_1_name = "Custom Text 1"
        self.template.get_custom_text_1 = "row['CustomText1']"

    def build(self):
        self.template.save()
        print("BankAccountTemplateBuilder: Created test bank account template with id "
              + str(self.template.id))
        return self.template

    @classmethod
    def write_transactions_to_file(cls, file_path, transactions):
        file_ = open(file_path, "w")
        file_.write('"Date","Description","CustomDate1","CustomText1","Amount","CurrentBalance","Label","Notes"')
        for transaction in transactions:
            values = [
                transaction.date.__format__("%d/%m/%y"),
                transaction.description,
                transaction.custom_date_1.__format__("%d/%m/%y") if transaction.custom_date_1 is not None else "",
                transaction.custom_text_1,
                str(transaction.amount),
                str(transaction.current_balance),
            ]
            file_.write("\n" + ",".join(values))
        file_.close()
