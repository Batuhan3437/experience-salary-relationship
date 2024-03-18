import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from pymongo import MongoClient

df = pd.read_csv("reading_data/polynomial.csv", sep=";")

# 'deneyim' sütununu sayısal değere dönüştürme
df['deneyim'] = df['deneyim'].astype(float)

# Dereceyi grafiğe göre en uygununu seçerek bulduk
polynomial_regression = PolynomialFeatures(degree=4)
x_polynomial = polynomial_regression.fit_transform(df[['deneyim']])

reg = LinearRegression()
reg.fit(x_polynomial, df['maas'])

print("=============================\n")
print("Maaş Tahmin Edici Yapay Zeka")
print("\n=============================\n")

# MongoDB connection
client = MongoClient("""'MongoDb bağlantı'""")
db = client['deneyim']
collection = db['maas']

while True:
    deneyim_ = float(input("Deneyiminiz kaç sene (yıl olarak giriniz): "))

    if deneyim_ > 0 and deneyim_ < 40:
        x_polynomial1 = polynomial_regression.transform([[deneyim_]])

        sonuc = int(reg.predict(x_polynomial1))
        formatted_x = "{0:,}".format(sonuc).replace(",", ".")

        print("\n=============================\n")
        print("Maaşınızın tahmini fiyatı:", formatted_x, "₺")
        print("\n=============================\n")

        # MongoDB'ye veri ekleme
        document = {'Deneyim (yıl)': deneyim_, 'maas': formatted_x}
        collection.insert_one(document)

        break
    elif deneyim_ >= 40:
        print("\n\nBundan sonra çalışmasanız sağlığınız için daha iyi olur.\n\n")
        break
    else:
        print("\n\nYanlış bir deneyim değeri girdiniz. Tekrar deneyin.\n\n")
        continue

# Bağlantıyı kapatın
client.close()
