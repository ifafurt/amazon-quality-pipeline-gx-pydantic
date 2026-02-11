import great_expectations as gx
import pandas as pd
import requests
import sys
import socketserver
import os
from dotenv import load_dotenv

# 1. WINDOWS & PYTHON 3.13 UYUMU
if sys.platform == 'win32':
    socketserver.UnixStreamServer = socketserver.TCPServer
    socketserver.UnixStreamHandler = socketserver.StreamRequestHandler

# 2. VERİYİ YÜKLE
file_path = "Amazon Sale Report.csv"
df = pd.read_csv(file_path, low_memory=False)

# 3. GX CONTEXT
context = gx.get_context()

# 4. VERİ KAYNAĞI VE ASSET
try:
    context.data_sources.delete("amazon_source")
except:
    pass

data_source = context.data_sources.add_pandas(name="amazon_source")
data_asset = data_source.add_dataframe_asset(name="amazon_asset")
batch_definition = data_asset.add_batch_definition_whole_dataframe("amazon_batch_def")

# 5. BEKLENTİ SETİ (SUITE)
suite = context.suites.add(gx.ExpectationSuite(name="amazon_suite"))

# Kurallar (Ödev Maddeleri)
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="Order ID"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="Order ID"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="Qty", min_value=0))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="Amount", min_value=0))

allowed_statuses = ["Cancelled", "Shipped", "Shipped - Delivered to Buyer", "Pending", "Unshipped"]
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(column="Status", value_set=allowed_statuses))

# 6. VALIDASYON TANIMI
validation_def = context.validation_definitions.add(
    gx.ValidationDefinition(name="amazon_validation", data=batch_definition, suite=suite)
)

# 7. ÇALIŞTIR
print("Validasyon hesaplanıyor...")
result = validation_def.run(batch_parameters={"dataframe": df})

# 8. SONUÇLARI TERMİNALDE GÖSTER (Düzeltilmiş Kısım)
print("\n" + "="*50)
print(f"VERİ KALİTESİ SONUCU: {'✅ BAŞARILI' if result.success else '❌ HATALI'}")
print("="*50)

if not result.success:
    print("\nDetaylı Hata Listesi:")
    for res in result.results:
        if not res.success:
            # DÜZELTME: expectation_type yerine .type kullanıyoruz
            rule = res.expectation_config.type 
            col = res.expectation_config.kwargs.get("column")
            err_count = res.result.get("unexpected_count", 0)
            print(f"- {col} sütununda '{rule}' kuralı ihlal edildi. (Hatalı Satır Sayısı: {err_count})")
print("="*50)

# 9. SLACK BİLDİRİMİ
def send_slack(res):
    load_dotenv()
    webhook_url = os.getenv("webhook_url")
    if not webhook_url:
        print("❌ .env dosyasında webhook_url tanımlanmamış!")
        sys.exit(1)
    stats = res.statistics
    msg = f"""
*📊 Veri Kalitesi Özeti (Homework 1):* {'✅ BAŞARILI' if res.success else '❌ HATALI'}
- *Toplam Kontrol:* {stats['evaluated_expectations']}
- *Başarılı:* {stats['successful_expectations']}
- *Hatalı:* {stats['unsuccessful_expectations']}
- *Başarı Oranı:* %{stats['success_percent']:.2f}
    """
    try:
        requests.post(webhook_url, json={"text": msg})
        print("\nSlack bildirimi başarıyla gönderildi.")
    except:
        print("\nSlack URL'i eksik veya hatalı, bildirim atlanıyor.")

send_slack(result)