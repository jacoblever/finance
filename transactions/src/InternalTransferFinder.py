from itertools import groupby


class InternalTransferFinder:

    def __init__(self, all_transactions):
        self.all_transactions = list(all_transactions)

    def find(self):
        grouped = groupby(self.all_transactions, key=lambda x: x.date)
        matched_groups = []
        for date, transactions_today in grouped:
            transactions_today = list(transactions_today)

            today_groups = []
            for transaction in transactions_today:
                matches = [x for x in transactions_today if
                       x.amount == -transaction.amount or x.amount == transaction.amount]
                ids = [x.id for x in matches]
                ids.sort()
                if today_groups.__contains__(ids) or len(ids) == 1:
                    continue
                if len(set([x.amount for x in matches])) == 1:
                    continue

                today_groups.append(ids)
                matched_groups.append(matches)

        return matched_groups
