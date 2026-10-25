import matplotlib.pyplot as plt

# 1. Prepare Data
years = [2023, 2024, 2025, 2026]
revenue = [15, 25, 30, 45]

# 2. Create the Plot
plt.plot(years, revenue, marker='o', color='b', linestyle='--')

# 3. Customize Labels
plt.title("Company Revenue Growth (2023-2026)")
plt.xlabel("Year")
plt.ylabel("Revenue (in $ Millions)")
plt.grid(True)

# 4. Display or Save
plt.savefig("revenue_chart.png")
plt.show()
