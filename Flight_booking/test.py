
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path="key.env")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(supabase_url, supabase_key)

birthday = datetime.strptime('2023-1-1', "%Y-%m-%d").strftime("%Y-%m-%d")

print(birthday)

passenger_data = {
    'username': 'aaaa',
    'firstname': 'Wanting',
    'lastname': 'Huang',
    'idnumber': '123456',
    'emailaddress': 'ttrbbkry@gmail.com',
    'phone': '1234567891',
    'birthday': '2023-01-01',
    'addressline1': '101 st',
    'addressline2': '102 st',
    'country': 'Canada',
    'city': 'Kingston',
    'postalcode': 'k7l 1c5',
    'emergfirstname': 'amanda',
    'emerglastname': 'xiang',
    'emergphone': '9876543211',
    'emergemailaddress': '20wh18@queensu.ca'
}

try:
    # 尝试插入数据
    response = supabase.table("passenger_information").insert(passenger_data).execute()

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