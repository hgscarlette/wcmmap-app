import pandas as pd

# Read WCM store data
df = pd.read_excel(r"data\Winmart location.xlsx")

# Read Winpay stores
winpay_stores = pd.read_excel(r"data\WMP store select (20241211) add data HN+HCM.xlsx", sheet_name="50 stores selected", skiprows = 4, usecols="A")
winpay_stores["SAP code"] = winpay_stores["SAP code"].apply(str)

# Add an indicator to tell whether a WCM store is using Winpay solution
df["is_winpay"] = 0
df.loc[df.STORE_ID.isin(winpay_stores["SAP code"]), "is_winpay"] = 1
df.insert(2, "is_winpay", df.pop("is_winpay"))

# Save the updated store data
df.to_csv(r"data\WCM stores_ext.csv", index=False)