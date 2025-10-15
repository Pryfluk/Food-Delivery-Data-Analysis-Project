import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.font_manager.fontManager.addfont('THSarabunNew.ttf') # 3.2+
mpl.rc('font', family='TH Sarabun New')

df = pd.read_csv('food_delivery_comparison.csv')
df.isnull().sum()
df.to_csv("cleaned_food_delivery_data.csv", index=False)

df.rename(columns={"Platform": "Brand"}, inplace=True)
df.rename(columns={"Restaurant Type": "Type"}, inplace=True)
df.rename(columns={"Delivery Time (min)": "Time"}, inplace=True)
df.rename(columns={"Number of Restaurants": "Restaurants"}, inplace=True)
df.rename(columns={"Delivery Fee (THB)": "Delivery Price"}, inplace=True)
df.rename(columns={"Avg Food Price (THB)": "Food Price"}, inplace=True)

df1 = df[df['Brand'] == 'GrabFood']
df2 = df[df['Brand'] == 'Robinhood']

#หาค่าเฉลี่ยของแต่ละคอลัมน์ของทั้งสองแบรนด์
grabfood_avg = df1[['Time', 'Delivery Price', 'Food Price', 'Avg Rating']].mean()

robinhood_avg = df2[['Time', 'Delivery Price', 'Food Price', 'Avg Rating']].mean()

print("GrabFood Averages:")
print(grabfood_avg)

print("\nRobinhood Averages:")
print(robinhood_avg)

#เปรียบเทียบค่าเฉลี่ยทุกอย่างของทั้งสองแบรนด์
labels = ['ระยะเวลาจัดส่ง (min)', 'ค่าจัดส่ง (THB)', 'ค่าอาหาร (THB)', 'ค่าเฉลี่ยเรทติ้ง']
grabfood_values = [grabfood_avg['Time'], grabfood_avg['Delivery Price'], grabfood_avg['Food Price'], grabfood_avg['Avg Rating']]
robinhood_values = [robinhood_avg['Time'], robinhood_avg['Delivery Price'], robinhood_avg['Food Price'], robinhood_avg['Avg Rating']]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, grabfood_values, width, label='GrabFood', color='lime')
bars2 = ax.bar(x + width/2, robinhood_values, width, label='Robinhood', color='indigo')

ax.set_xlabel('Metrics')
ax.set_ylabel('ค่าเฉลี่ย')
ax.set_title('เปรียบเทียบระหว่าง Grab กับ Robinhood')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(bars1)
add_labels(bars2)

plt.tight_layout()
plt.show()

# รวมจำนวนร้านอาหารตามพื้นที่สำหรับแต่ละแบรนด์
grabfood_restaurants_by_area = df1.groupby('Area')['Restaurants'].sum()
robinhood_restaurants_by_area = df2.groupby('Area')['Restaurants'].sum()

fig, ax = plt.subplots(1, 2, figsize=(14, 6))
ax[0].pie(grabfood_restaurants_by_area, labels=grabfood_restaurants_by_area.index, autopct='%1.1f%%', startangle=90)
ax[0].set_title('สัดส่วนของ GrabFood ในแต่ละจังหวัด')

ax[1].pie(robinhood_restaurants_by_area, labels=robinhood_restaurants_by_area.index, autopct='%1.1f%%', startangle=90)
ax[1].set_title('สัดส่วนของ Robinhood ในแต่ละจังหวัด')

plt.tight_layout()
plt.show()

#Relationship ระหว่าง Price กับ Rating
plt.figure(figsize=(10, 6))
plt.scatter(df1['Food Price'], df1['Avg Rating'], color='orange', label='GrabFood', alpha=0.7)
plt.scatter(df2['Food Price'], df2['Avg Rating'], color='blue', label='Robinhood', alpha=0.7)

plt.xlabel('ราคาอาหารเฉลี่ย (บาท)')
plt.ylabel('คะแนนเรทติ้ง')
plt.title('ความสัมพันธ์ของราคาอาหาร กับ คะแนนเรทติ้ง')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()