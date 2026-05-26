import csv
import sys

try:
    import requests
except ImportError:
    requests = None
    import urllib.request
    import ssl

URL = "https://data.kcg.gov.tw/File/DirectDownload/7829e6a5-9176-4072-b801-185f33c82095"


def fetch_csv_text(url):
    if requests:
        response = requests.get(url, timeout=15, verify=False)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        content = response.content
        return content, content_type
    else:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, timeout=15, context=context) as response:
            content = response.read()
            content_type = response.headers.get("Content-Type", "")
            return content, content_type


def main():
    try:
        content, content_type = fetch_csv_text(URL)
    except Exception as exc:
        print(f"無法擷取資料: {exc}")
        sys.exit(1)

    byte_length = len(content)
    text = content.decode("utf-8-sig")
    rows = list(csv.reader(text.splitlines()))

    if not rows:
        print("未找到任何資料。")
        return

    header = rows[0]
    data_rows = rows[1:]
    total_rows = len(data_rows)
    field_count = len(header)

    print("==== 讀取結果 ====\n")
    print(f"目標 URL: {URL}")
    print(f"Content-Type: {content_type}")
    print(f"資料長度: {byte_length} bytes\n")

    print(f"總列數: {total_rows}, 欄位數: {field_count}\n")

    if total_rows > 0:
        first_row = data_rows[0]
        print("==== 第1筆資料 ====\n")
        for key, value in zip(header, first_row):
            value = value.strip()
            if key == "Description" and not value:
                value = "無"
            print(f"{key} : {value}")


if __name__ == "__main__":
    main()
