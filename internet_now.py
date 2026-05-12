import requests
from datetime import datetime
import pytz

def get_internet_time():
    try:
        # Make a HEAD request to get server time
        response = requests.head("https://apigateway.tencentcloudapi.com", timeout=5)
        response.raise_for_status()  # Raise exception for bad status codes

        # Get the Date header from response
        server_time = response.headers["Date"]
        print("腾讯云服务器时间（GMT）：", server_time)

        # Parse GMT time and convert to Shanghai time
        dt_gmt = datetime.strptime(server_time, "%a, %d %b %Y %H:%M:%S %Z")
        dt_gmt = dt_gmt.replace(tzinfo=pytz.UTC)  # Make it timezone-aware
        dt_shanghai = dt_gmt.astimezone(pytz.timezone('Asia/Shanghai'))

        print("腾讯云时间 (上海时区):", dt_shanghai)

        return dt_shanghai

    except requests.exceptions.RequestException as e:
        print(f"获取网络时间失败: {e}")
        return None


def is_time_hit(target_time="22:00"):
    internet_time = get_internet_time()
    if not internet_time:
        print("无法获取网络时间，使用本地时间")
        internet_time = datetime.now(pytz.timezone('Asia/Shanghai'))

    # Parse target time (today's date with target HH:MM)
    today = internet_time.date()
    target_datetime = datetime.strptime(f"{today} {target_time}", "%Y-%m-%d %H:%M:%S")
    target_datetime = pytz.timezone('Asia/Shanghai').localize(target_datetime)

    # Compare times (allow 1-minute tolerance)
    time_diff = abs((internet_time - target_datetime).total_seconds())

    if time_diff <= 1:  # 1 minute tolerance
        print(f"✅ 当前时间 {internet_time.strftime('%H:%M')} 匹配目标时间 {target_time}")
        return True
    else:
        print(
            f"❌ 当前时间 {internet_time.strftime('%H:%M')} 未匹配目标时间 {target_time} (偏差: {int(time_diff)} 秒)")
        return False



