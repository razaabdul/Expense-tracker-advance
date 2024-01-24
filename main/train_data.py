import random
import pandas as pd
from faker import Faker

# Create a list of expense types
expense_types = ["Rent", "Mobile Recharge", "Transport", "Water", "Electricity"]

# Initialize Faker to generate user names
fake = Faker()

# Initialize an empty list to store the data
data = []

# Generate 1000 lines of data
for _ in range(1000):
    user = fake.first_name()
    expense_type = random.choice(expense_types)
    transaction_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
    amount = random.randint(50, 5000)
    mode = random.choice(["Gpay", "Paytm", "Cash"])

    data.append([user, expense_type, transaction_date, amount, mode])

# Create a DataFrame from the generated data
df = pd.DataFrame(data, columns=["User", "Expense_Type", "Transaction_Date", "Amount", "Mode"])

# Save the data to an Excel file
df.to_excel("expense_data.xlsx", index=False)
