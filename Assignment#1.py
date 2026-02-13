import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

# PART 1: Load the Kaggle Dataset

df = pd.read_csv("data/train.csv")
df.columns = df.columns.str.lower()
df["approx_days_on_market"] = (df["yrsold"] - df["yearbuilt"]) * 30
df = df[df["approx_days_on_market"] < 365]
df["open_floor_plan"] = df["totrmsabvgrd"] > 7
df["large_home"] = df["grlivarea"] > df["grlivarea"].median()

# PART 2: Scrape Small Subset

url = "https://en.wikipedia.org/wiki/House"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
paragraphs = soup.find_all("p")
sample_text = " ".join([p.get_text() for p in paragraphs[:5]])
scraped_data = {
    "source": "wikipedia",
    "text_sample_length": len(sample_text)
}
scraped_df = pd.DataFrame([scraped_data])

# PART 3: Exploratory Analysis

median_dom_open = df.groupby("open_floor_plan")["approx_days_on_market"].median()
median_dom_size = df.groupby("large_home")["approx_days_on_market"].median()
summary_table = pd.DataFrame({
    "Median_DOM_Open_Floor_Plan": median_dom_open,
    "Median_DOM_Large_Home": median_dom_size
})

print("\nSummary Table:")
print(summary_table)

plt.figure()
sns.boxplot(x="open_floor_plan", y="approx_days_on_market", data=df)
plt.title("Days on Market vs Open Floor Plan")
plt.xlabel("Open Floor Plan (True/False)")
plt.ylabel("Approx Days on Market")
plt.show()

# PART 4: Save Cleaned Data

df.to_csv("data/cleaned_housing_data.csv", index=False)
