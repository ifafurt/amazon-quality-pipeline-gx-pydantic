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
validation_definition = context.validation_definitions.add(
    gx.ValidationDefinition(name="amazon_validation", data=batch_definition, suite=suite)
)

# 7. ÇALIŞTIR
print("Calculating validation...")
validation_result = validation_definition.run(batch_parameters={"dataframe": df})

# 8. SONUÇLARI TERMİNALDE GÖSTER (Düzeltilmiş Kısım)
print("\n" + "="*50)
print(f"DATA QUALITY RESULT: {'✅ SUCCESS' if validation_result.success else '❌ FAILED'}")
print("="*50)

if not validation_result.success:
    print("\nDetailed Error List:")
    for res in validation_result.results:
        if not res.success:
            # DÜZELTME: expectation_type yerine .type kullanıyoruz
            rule = res.expectation_config.type 
            column_name = res.expectation_config.kwargs.get("column")
            unexpected_count = res.result.get("unexpected_count", 0)
            print(f"- Column '{column_name}' failed rule '{rule}'. (Unexpected Count: {unexpected_count})")
print("="*50)

# 9. SLACK BİLDİRİMİ
def send_slack_notification(result_data):
    load_dotenv()
    webhook_url = os.getenv("webhook_url")
    
    if not webhook_url:
        print("ℹ️ Info: webhook_url is not defined in .env or Secrets, skipping Slack notification.")
        return # Pipeline'ın çökmemesi için sys.exit(1) yerine return kullandım

    stats = result_data.statistics
    status_msg = '✅ SUCCESS' if result_data.success else '❌ FAILED'
    
    msg = f"""
*📊 Data Quality Summary (Homework 1):* {status_msg}
- *Total Checks:* {stats['evaluated_expectations']}
- *Successful:* {stats['successful_expectations']}
- *Failed:* {stats['unsuccessful_expectations']}
- *Success Rate:* {stats['success_percent']:.2f}%
    """
    
    try:
        response = requests.post(webhook_url, json={"text": msg})
        if response.status_code == 200:
            print("\nSlack notification sent successfully.")
        else:
            print(f"\nSlack returned an error: {response.status_code}")
    except Exception as e:
        print(f"\nFailed to send Slack notification: {e}")

send_slack_notification(validation_result)