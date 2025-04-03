from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time



def date(a):
    date = a.split('(')[0].strip()     
    month, day = map(int, date.split('/'))
    return datetime(1111, month, day, 1, 1).strftime("%m月%d日")

def format_time(b):
    hour, minute = map(int, b.split(':'))
    return datetime(1111, 1, 1, hour, minute).strftime("%H:%M")

def get_background_class():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 10:  
        return "from-yellow-300 to-orange-500"
    elif 10 <= current_hour < 17:  
        return "from-blue-400 to-indigo-600"
    elif 17 <= current_hour < 20:  
        return "from-orange-500 to-pink-600"
    else:  
        return "from-gray-800 to-black"

def fetch_weather():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)




    url = "https://www.cwa.gov.tw/V8/C/W/Town/Town.html?TID=6301100"
    driver.get(url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    original_time = soup.find("span", class_="GT_Time").text.strip()
    current_date = date(original_time)

    Rhum = int(soup.find("span", class_="GT_RH").text.strip().replace("%", ""))

    temp = int(soup.find("span", class_="GT_T").find("span", class_="tem-C").text.strip())
    Atemp = int(soup.find("span", class_="GT_AT").find("span", class_="tem-C").text.strip())

    original_sunrise = soup.find("span", class_="GT_Sunrise").text.strip()
    sunrise = format_time(original_sunrise)  

    original_sunset = soup.find("span", class_="GT_Sunset").text.strip()
    sunset = format_time(original_sunset)   

    background_class = get_background_class()  

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>天氣應用</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @keyframes gradient-animation {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .animated-bg {{
                background: linear-gradient(270deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
                background-size: 400% 400%;
                animation: gradient-animation 15s ease infinite;
            }}

        </style>
        <script>
            function adjustTextColor() {{
                const body = document.body;
                const computedStyle = window.getComputedStyle(body);
                const bgColor = computedStyle.backgroundImage;

                const colors = bgColor.match(/rgb\\(.*?\\)/g);
                if (!colors) return;

                const luminance = colors.map(color => {{
                    const rgb = color.match(/\\d+/g).map(Number);
                    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
                }});
                const avgLuminance = luminance.reduce((a, b) => a + b, 0) / luminance.length;

                const textColor = avgLuminance > 128 ? "black" : "white";
                body.style.color = textColor;
            }}

            window.onload = adjustTextColor;
            window.onresize = adjustTextColor;
        </script>
    </head>


    <body class="animated-bg min-h-screen flex items-center justify-center">
        <div class="text-center p-6 rounded-3xl bg-white/10 backdrop-blur-lg shadow-lg w-80">
            <h1 class="text-2xl font-semibold">台北 士林區</h1>
            <p class="text-sm">{current_date}</p>
            <div class="my-6">
                <img src="https://cdn-icons-png.flaticon.com/512/1163/1163661.png" alt="天氣圖示" class="w-24 mx-auto">
                <p class="text-5xl font-bold">{temp}°C</p>
                <p class="text-lg">體感溫度: {Atemp}%</p>
            </div>
            <div class="flex justify-between text-sm mt-4">
                <div>
                    <p>日出時間</p>
                    <p class="font-semibold">{sunrise}</p>
                </div>
                <div>
                    <p>相對濕度</p>
                    <p class="font-semibold">{Rhum}%</p>
                </div>
                <div>
                    <p>日落時間</p>
                    <p class="font-semibold">{sunset}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    with open("weather.html", "w", encoding="utf-8") as file:
        file.write(html_content)


schedule.every(1).hours.do(fetch_weather)

try:
    fetch_weather()
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nOAO")