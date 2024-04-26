from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

@app.route('/import-customers', methods=['POST'])
def import_customers():
    # Nhận dữ liệu JSON từ request
    json_data = request.get_json()

    # Kết nối đến database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Xóa dữ liệu cũ khỏi bảng (nếu có)
    c.execute('DELETE FROM Customer')

    # Duyệt qua danh sách khách hàng trong JSON
    for customer_data in json_data['customers']:
        first_name = customer_data['first_name']
        last_name = customer_data['last_name']
        email = customer_data['email']
        phone_number = customer_data['phone_number']
        address = customer_data['address']

        # INSERT dữ liệu vào bảng Customer
        c.execute("""INSERT INTO Customer (first_name, last_name, email, phone_number, address)
                     VALUES (?, ?, ?, ?, ?)""",
                  (first_name, last_name, email, phone_number, address))
    # Cam kết thay đổi
    conn.commit()

    # Đóng kết nối
    conn.close()

    # Trả về thông báo thành công
    return jsonify({"success": True, "message": "Customers imported successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
