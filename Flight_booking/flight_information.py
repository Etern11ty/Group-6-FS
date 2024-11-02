import requests
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# 加载Supabase和API密钥
load_dotenv(dotenv_path="key.env")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# 直接设置API密钥
aviationstack_api_key = "2e500ee8ee507d60e008dbda034379f0"

# 初始化Supabase客户端
supabase: Client = create_client(supabase_url, supabase_key)

def fetch_routes():
    # 定义API请求的URL和参数
    url = "http://api.aviationstack.com/v1/routes"
    
    params = {
        'access_key': aviationstack_api_key,
        'limit': 10,  # 获取前10条数据
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    # 检查是否成功获取数据
    if 'data' in data:
        for route in data['data']:
            # 从API响应中提取相关信息
            route_info = {
                'flight_number': route.get('flight', {}).get('iata', 'Unknown'),
                'departure': route.get('departure', {}).get('airport', 'Unknown'),
                'destination': route.get('arrival', {}).get('airport', 'Unknown'),
                'plane_model': route.get('aircraft', {}).get('model', 'Unknown')
            }
            
            # 插入数据到Supabase
            response = supabase.table("flight_information").insert(route_info).execute()
            print(f"Inserted route {route_info['flight_number']}: {response.data}")

    else:
        print("Failed to fetch route data:", data.get("error", "Unknown error"))

# 调用函数获取并存储航线信息
fetch_routes()