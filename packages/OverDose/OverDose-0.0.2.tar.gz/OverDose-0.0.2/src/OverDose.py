import pandas as pd
import subprocess as sp
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

sp.call('wget -nc https://github.com/i-inose/OverDose/raw/main/VSRR_Provisional_Drug_Overdose_Death_Counts.csv', shell=True)
data = pd.read_csv('VSRR_Provisional_Drug_Overdose_Death_Counts.csv')
desired_indicators = ["Cocaine (T40.5)", "Psychostimulants with abuse potential (T43.6)", "Heroin (T40.1)", "Opioids (T40.0-T40.4,T40.6)"]
filtered_data = data[(data["Indicator"].isin(desired_indicators)) & (data["State"] == "US") & (data["Year"] != 2023)]
aggregated_data = filtered_data.pivot_table(index="Year", columns="Indicator", values="Data Value", aggfunc="sum")

plt.figure(figsize=(10, 6))
aggregated_data.plot(linewidth=2, color=['black', 'black', 'black', 'black'], style=['-', '--', '-.', ':'], ax=plt.gca())
plt.title("Drug Overdose Death Counts by Indicator (2015-2022)")
plt.xlabel("Year")
plt.ylabel("Death Counts")
plt.legend(title="Indicator", labels=desired_indicators)
ax = plt.gca()
ax.get_yaxis().set_major_formatter(ScalarFormatter())
ax.yaxis.get_major_formatter().set_scientific(False)
fig = plt.figure(1)

def main():
	plt.savefig('result.png',dpi=fig.dpi,bbox_inches='tight')
	plt.grid(True)
	plt.show()

if __name__ == "__main__":
	main()
