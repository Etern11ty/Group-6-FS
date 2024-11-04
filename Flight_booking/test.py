
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path="key.env")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(supabase_url, supabase_key)


booking_data = {
        "username": 'abc',
        "flightnumber": 'flight_info.get('')',
        "purchase_time": "now()",
        "first_name": 'passenger_info.get('')',
        "last_name": 'passenger_info.get('')',
    }

    # Insert data into Supabase `bookinghistory` table
try:
    response = supabase.table("bookinghistory").insert(booking_data).execute()
    if response.error:
        print(f"Error saving booking: {response.error}")  # 打印错误信息

    # 打印完整的响应对象以检查结构
    print("Supabase 完整响应:", response)

    # 检查响应对象是否包含 status_code 和 data 等信息
    if hasattr(response, 'status_code'):
        print("状态码:", response.status_code)

    if hasattr(response, 'data'):
        print("数据:", response.data)

    if hasattr(response, 'error'):
        print("错误信息:", response.error)  # 如果 error 存在，打印错误信息

    # 基于 data 属性判断插入是否成功
    if response.data:
        print("数据插入成功!")
    else:
        print("没有返回数据，插入可能失败。")

except Exception as e:
    # 捕获任何异常并打印错误
    print(f"在尝试插入数据到 Supabase 时发生错误: {e}")