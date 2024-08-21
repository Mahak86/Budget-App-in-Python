class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f'{self.name:*^30}\n'
        items = ''
        for item in self.ledger:
            amount = f"{item['amount']:7.2f}"
            description = item['description'][:23]
            items += f'{description:<23}{amount:>7}\n'
        total = f'Total: {self.get_balance():.2f}'
        return title + items + total


def create_spend_chart(categories):
    total_withdrawals = sum(
        sum(item['amount'] for item in category.ledger if item['amount'] < 0) for category in categories)
    
    chart = 'Percentage spent by category\n'
    percentages = [
        sum(item['amount'] for item in category.ledger if item['amount'] < 0) / total_withdrawals * 100
        for category in categories
    ]
    
    for i in range(100, -1, -10):
        chart += f'{i:>3}|'
        for percentage in percentages:
            chart += ' o ' if percentage >= i else '   '
        chart += ' \n'
    
    chart += '    ----------\n'
    
    max_len = max(len(category.name) for category in categories)
    names = [category.name.ljust(max_len) for category in categories]
    
    for i in range(max_len):
        chart += '     ' + ''.join(name[i] + '  ' for name in names) + '\n'
    
    return chart.rstrip('\n')
