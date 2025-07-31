from flask import Flask, render_template, request, redirect, send_file
import csv
import pandas as pd

app = Flask(__name__)

ADMIN_PASSWORD = "evn3862"  # đổi mật khẩu tại đây
CSV_FILE = 'data.csv'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = [
        request.form['name'],
        request.form['zalo'],
        request.form['phone'],
        request.form['uid']
    ]
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    return "Đã ghi thông tin!"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            # Đọc CSV -> tạo Excel
            df = pd.read_csv(CSV_FILE, header=None, names=["Tên ingame", "Tên Zalo", "SĐT", "ID Game"])
            excel_file = 'data.xlsx'
            df.to_excel(excel_file, index=False, engine='openpyxl')

            return send_file(
                excel_file,
                as_attachment=True,
                download_name='data.xlsx'
            )
        else:
            return "Sai mật khẩu!"
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
