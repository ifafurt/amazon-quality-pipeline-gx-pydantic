#pydantic_check.py
import sys
import pandas as pd
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
import requests
import os
from dotenv import load_dotenv

# 1. SATIR MODELİ (Her bir satırın uyması gereken kurallar)
class AmazonOrderModel(BaseModel):
    # Field(alias=...) ile CSV'deki boşluklu başlıkları Python değişkenine bağlıyoruz
    order_id: str = Field(alias="Order ID")
    qty: int = Field(alias="Qty", ge=0)
    amount: Optional[float] = Field(alias="Amount", ge=0)
    currency: str = Field(alias="currency")
    ship_country: str = Field(alias="ship-country")
    date: str = Field(alias="Date")

    model_config = ConfigDict(populate_by_name=True)

    # ÖDEV KURALI: Para birimi sadece "INR" olmalı
    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):
        if v != "INR":
            raise ValueError(f"Invalid currency: {v}. Only INR is accepted.")
        return v

    # ÖDEV KURALI: Ülke sadece "IN" olmalı
    @field_validator("ship_country")
    @classmethod
    def validate_country(cls, v):
        if v != "IN":
            raise ValueError(f"Invalid country: {v}. Only IN is accepted.")
        return v

# 2. VERİYİ YÜKLE
df = pd.read_csv("Amazon Sale Report.csv", low_memory=False)

valid_rows = []
invalid_rows = []

print("Starting row-level validation...")

# 3. SATIRLARI DÖNGÜYE AL VE KONTROL ET
for index, row in df.iterrows():
    # Satırı sözlüğe (dict) çeviriyoruz
    row_dict = row.to_dict()
    
    try:
        # Pydantic satırı doğrulamaya çalışır
        AmazonOrderModel(**row_dict)
        valid_rows.append(row_dict)
    except Exception as e:
        # Hata varsa, hatayı da satıra ekleyip 'invalid' listesine atıyoruz
        row_dict["error_details"] = str(e)
        invalid_rows.append(row_dict)

# 4. SONUÇLARI KAYDET
pd.DataFrame(valid_rows).to_csv("valid_rows.csv", index=False)
pd.DataFrame(invalid_rows).to_csv("invalid_rows.csv", index=False)

print(f"Validation process completed!")
print(f"✅ Valid rows count: {len(valid_rows)}")
print(f"❌ Invalid rows count: {len(invalid_rows)}")

# 5. SLACK BİLDİRİMİ (Eğer hata varsa)
if invalid_rows:
    load_dotenv()
    webhook_url = os.getenv("webhook_url")
    if not webhook_url:
        print("ℹ️ Info: webhook_url is not defined in .env or Secrets, skipping Slack notification.")
    else:
        msg = f"⚠️ *Pydantic Alert:* {len(invalid_rows)} rows failed data quality validation and were extracted."
        try:
            requests.post(webhook_url, json={"text": msg})
            print("Slack alert sent.")
        except Exception as error:
            print(f"Could not send Slack alert: {error}")