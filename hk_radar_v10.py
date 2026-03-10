import requests
import time

SENDKEY = "SCT310785TyiuMic8XVy7CLH0GhULNvBej"


def send_wechat(title, msg):

    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"

    data = {
        "title": title,
        "desp": msg
    }

    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass


stocks = {

"腾讯": ("0700.HK","互联网"),
"阿里巴巴": ("9988.HK","互联网"),
"美团": ("3690.HK","互联网"),
"小米": ("1810.HK","互联网"),
"京东": ("9618.HK","互联网"),
"网易": ("9999.HK","互联网"),
"百度": ("9888.HK","互联网"),
"快手": ("1024.HK","互联网"),
"哔哩哔哩": ("9626.HK","互联网"),

"理想汽车": ("2015.HK","新能源车"),
"小鹏汽车": ("9868.HK","新能源车"),
"蔚来": ("9866.HK","新能源车"),
"比亚迪": ("1211.HK","新能源车"),
"吉利汽车": ("0175.HK","新能源车"),
"长城汽车": ("2333.HK","新能源车"),

"中芯国际": ("0981.HK","半导体"),
"华虹半导体": ("1347.HK","半导体"),

"舜宇光学": ("2382.HK","消费电子"),
"瑞声科技": ("2018.HK","消费电子"),
"比亚迪电子": ("0285.HK","消费电子"),

"海底捞": ("6862.HK","消费"),
"农夫山泉": ("9633.HK","消费"),
"安踏": ("2020.HK","消费"),
"李宁": ("2331.HK","消费"),

"中国移动": ("0941.HK","电信"),
"中国联通": ("0762.HK","电信"),
"中国电信": ("0728.HK","电信"),

"友邦保险": ("1299.HK","金融"),
"汇丰控股": ("0005.HK","金融"),
"港交所": ("0388.HK","金融"),
"中国平安": ("2318.HK","金融"),

"招商银行": ("3968.HK","银行"),
"工商银行": ("1398.HK","银行"),
"建设银行": ("0939.HK","银行"),
"农业银行": ("1288.HK","银行"),
"中国银行": ("3988.HK","银行"),

"中国海油": ("0883.HK","能源"),
"中国石油": ("0857.HK","能源"),
"中国石化": ("0386.HK","能源")

}


def get_data(code):

    url = f"https://stooq.com/q/d/l/?s={code}&i=d"

    try:

        r = requests.get(url, timeout=10)

        lines = r.text.split("\n")

        if len(lines) < 22:
            return None

        data = []

        for line in lines[1:]:

            if line.strip() == "":
                continue

            row = line.split(",")

            close = float(row[4])
            volume = float(row[5])
            high = float(row[2])

            data.append((close, volume, high))

        return data[-21:]

    except:

        return None


def scan():

    print("扫描股票数量:", len(stocks))

    signals = []
    sector_count = {}

    for name,(code,sector) in stocks.items():

        try:

            data = get_data(code)

            if not data:
                continue

            closes = [d[0] for d in data]
            volumes = [d[1] for d in data]
            highs = [d[2] for d in data]

            close_today = closes[-1]
            close_yesterday = closes[-2]

            volume_today = volumes[-1]

            vol20 = sum(volumes[:-1]) / 20

            change = (close_today - close_yesterday) / close_yesterday * 100

            ma5 = sum(closes[-5:]) / 5
            ma10 = sum(closes[-10:]) / 10
            ma20 = sum(closes[-20:]) / 20

            volume_ratio = volume_today / vol20

            high20 = max(highs[:-1])

            trend = "趋势一般"

            if ma5 > ma10 > ma20:
                trend = "多头排列"

            print(
                name,
                round(change,2),"%",
                round(volume_ratio,2),"倍",
                "MA5:",round(ma5,2),
                "MA10:",round(ma10,2),
                "MA20:",round(ma20,2),
                trend
            )

            signal = None


            if volume_ratio > 1.5 and change > 3:
                signal = "主力启动"

            elif close_today > high20 and volume_ratio > 1.3:
                signal = "突破信号"

            elif ma5 > ma10 > ma20 and change > 2:
                signal = "趋势加速"

            elif change > 7 and volume_ratio > 2:
                signal = "暴涨预警"


            if signal:

                signals.append((name,sector,signal,change,volume_ratio))

                sector_count[sector] = sector_count.get(sector,0) + 1

        except:
            continue

        time.sleep(0.4)


    if len(signals) == 0:
        print("没有发现交易信号")
        return


    message = ""

    for s in signals:

        message += f"""
股票：{s[0]}
板块：{s[1]}
信号：{s[2]}
涨幅：{round(s[3],2)}%
量能：{round(s[4],2)}倍

"""


    for sector,count in sector_count.items():

        if count >= 2:

            message += f"\n板块异动：{sector}\n"


    send_wechat("港股量化雷达 V10", message)


if __name__ == "__main__":

    scan()