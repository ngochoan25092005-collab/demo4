from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def fetch_data():
    # Đọc dữ liệu từ file 1.csv cục bộ
    file_path = r"d:\11242447\demo4\1.csv"
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            records = []
            for row in reader:
                # Bỏ qua các dòng phụ trong CSV (đánh dấu bằng dấu '-')
                if row.get('型式') == '-':
                    continue

                # Chuẩn hóa tên cột từ 1.csv để khớp với logic xử lý và index.html
                normalized_row = {
                    '行政區': row.get('行政區', ''),
                    '停車場名稱': row.get('場名', ''),
                    '種類': row.get('型式', ''),
                    '地址': row.get('位置', ''),
                    '大車': row.get('大車', '0'),
                    '小車': row.get('小車', '0'),
                    '機車': row.get('機車', '0'),
                    '緯度': row.get('緯度', ''),
                    '經度': row.get('經度', ''),
                    '收費標準': row.get('收費標準', ''),
                    '管理業者': row.get('管理業者', ''),
                    '聯絡電話': row.get('聯絡電話', ''),
                    '履約起迄': row.get('履約起迄', '')
                }
                records.append(normalized_row)
                
            print(f"成功讀取本地資料：共 {len(records)} 筆")
            return records

    except Exception as e:
        print(f"讀取本地檔案失敗: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    raw_data = fetch_data()
    
    # 取得篩選條件
    parking_type = request.form.get("parking_type", "")
    location = request.form.get("location", "")
    vehicle_type = request.form.get("vehicle_type", "")

    # 取得所有可選地名（行政區）
    location_options = sorted({item.get('行政區', '') for item in raw_data if item.get('行政區')})

    filtered_data = []
    for item in raw_data:
        # 1. 篩選停車形式 (平面/立體)
        type_match = True
        current_type = str(item.get('種類') or '')
        if parking_type and parking_type not in current_type:
            type_match = False
            
        # 2. 篩選地名 (模糊搜尋名稱或行政區)
        location_match = True
        if location:
            search_target = f"{item['停車場名稱']}{item['行政區']}{item['地址']}"
            if location not in search_target:
                location_match = False
                
        # 3. 篩選車輛種類 (檢查是否有該車種格位)
        vehicle_match = True
        if vehicle_type:
            try:
                val = int(item.get(vehicle_type, 0))
                if val <= 0:
                    vehicle_match = False
            except:
                vehicle_match = False

        if type_match and location_match and vehicle_match:
            filtered_data.append(item)

    return render_template(
        "index.html",
        data=filtered_data,
        parking_type=parking_type,
        location=location,
        vehicle_type=vehicle_type,
        location_options=location_options,
    )

if __name__ == "__main__":
    app.run(debug=True)
