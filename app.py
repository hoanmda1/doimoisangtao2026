from flask import Flask, request, render_template_string
import pandas as pd
from datetime import datetime

app = Flask(__name__)

form_html = '''
<h2>Phiếu điều tra dân số</h2>
<form method="POST">
  Họ và tên: <input type="text" name="name"><br><br>
  Tuổi: <input type="number" name="age"><br><br>
  Giới tính: 
    <select name="gender">
      <option value="Nam">Nam</option>
      <option value="Nữ">Nữ</option>
      <option value="Khác">Khác</option>
    </select><br><br>
  Địa phương: <input type="text" name="diaphuong"><br><br>
  Tên xã: <input type="text" name="tenxa"><br><br>
  Dân số: <input type="number" name="danso"><br><br>
  <input type="submit" value="Gửi phiếu">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'diaphuong': request.form['diaphuong'],
            'tenxa': request.form['tenxa'],
            'danso': request.form['danso']
        }

        # Đổi sang dataframe
        df_new = pd.DataFrame([data])

        # Tên file lưu
        file_name = "data.xlsx"
        try:
        # Nếu file đã tồn tại: đọc, nối thêm, rồi ghi đè
            df_existing = pd.read_excel(file_name)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        except FileNotFoundError:
    # Nếu chưa có file: ghi mới luôn
            df_combined = df_new
    # Ghi vào Excel
        df_combined.to_excel(file_name, index=False)

        return "<h3>Phiếu điều tra đã được lưu! Cảm ơn bạn.</h3>"

    return render_template_string(form_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)