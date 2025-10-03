class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        title = self.name.center(30, '*')
        items = ""
        total = 0
        for item in self.ledger:
            description = item['description'][:23].ljust(23)
            amount = "{:.2f}".format(item['amount']).rjust(7)
            items += f"{description}{amount}\n"
            total += item['amount']
        
        output = f"{title}\n{items}Total: {total:.2f}"
        return output

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

def create_spend_chart(categories):
    total_spent = 0
    spent_per_category = {}
    
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item['amount'] < 0:
                spent += abs(item['amount'])
        spent_per_category[category.name] = spent
        total_spent += spent

    chart = "Percentage spent by category\n"
    percentages = {name: int((spent / total_spent) * 100) // 10 * 10 for name, spent in spent_per_category.items()}

    for i in range(100, -1, -10):
        chart += f"{str(i).rjust(3)}| "
        for name in spent_per_category:
            if percentages[name] >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    -" + "---" * len(categories) + "\n"

    max_len = max(len(name) for name in spent_per_category)
    names = [name.ljust(max_len) for name in spent_per_category]

    for i in range(max_len):
        chart += "     "
        for name in names:
            chart += name[i] + "  "
        if i < max_len - 1:
            chart += "\n"

    return chart

food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")

food.deposit(1000, "initial deposit")
food.withdraw(150.15, "groceries")
food.withdraw(50.85, "restaurant and more")

entertainment.deposit(500, "initial deposit")
entertainment.withdraw(200, "movies")

business.deposit(1000, "initial deposit")
business.withdraw(300, "office supplies")

print(food)
print(entertainment)
print(business)

print(create_spend_chart([food, entertainment, business]))