import pandas as pd
import sqlite3

conn = sqlite3.connect("data/products.db")
df = pd.read_sql("SELECT * FROM product", conn)
print(df)
conn.close()