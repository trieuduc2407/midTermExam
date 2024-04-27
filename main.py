# C1
# a)
from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

sqldbname = 'MyDataBase.db'


# b)
@app.route('/', methods=['get'])
def index():
    info = '12_Dong Trieu Duc_De 2'
    return jsonify(info)


# C2
# a)
@app.route('/employee', methods=['get'])
def employee():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('SELECT * FROM Employee')
    result = c.fetchall()
    conn.close()
    return jsonify(result)


# b)
@app.route('/employee/<id>', methods=['delete'])
def delete_employee(id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('DELETE FROM Employee WHERE EmployeeID=?', (id,))
    conn.commit()
    conn.close()
    return 'employee deleted'


# C3
# a)
@app.route('/employee', methods=['post'])
def add_employee():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    ename = request.json.get('ename')
    aname = request.json.get('aname')
    email = request.json.get('email')
    password = request.json.get('password')
    tel = request.json.get('tel')
    department = request.json.get('department')
    role = request.json.get('role')
    c.execute(
        'insert into Employee (EmployeeName, AccountName, EmailAddress, Password, Tel, DepartmentID, RoleID) values (?,?,?,?,?,?,?)',
        (ename, aname, email, password, tel, department, role)
    )
    conn.commit()
    conn.close()
    return 'employee added'


# b)
@app.route('/employee/<id>', methods=['get', 'put'])
def update_employee(id):
    # Get old data from db
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('select * from Employee where EmployeeID = ?', (id,))
    old = c.fetchone()
    data = json.dumps(old)
    data = data[1:-1].replace('[', '').replace(']', '')
    old_formated = data.split(',')
    for i in range(0, len(old_formated)):
        old_formated[i] = old_formated[i].replace('"', '')
    # Get new data from json
    get_json = []
    get_json.append(request.json.get('ename'))
    get_json.append(request.json.get('aname'))
    get_json.append(request.json.get('email'))
    get_json.append(request.json.get('password'))
    get_json.append(request.json.get('tel'))
    get_json.append(request.json.get('department'))
    get_json.append(request.json.get('role'))
    for i in range(0, len(get_json)):
        if get_json[i] == None:
            continue
        else:
            old_formated[i+1] = get_json[i]
    # Cap nhat data moi vao DB
    for i in range(0, len(old_formated)):
        old_formated[i] = old_formated[i].lstrip()
    c.execute(
        'update Employee set EmployeeName=?, AccountName=?, EmailAddress=?, Password=?, Tel=?, DepartmentID=?, RoleID=? where EmployeeID=?',
        (old_formated[1], old_formated[2], old_formated[3], old_formated[4], old_formated[5], old_formated[6],
         old_formated[7], id)
    )
    conn.commit()
    conn.close()
    return jsonify(old_formated)


# C4
# a)
@app.route('/check', methods=['post'])
def check_employee_email_and_pass():
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    email = request.json.get('email')
    password = request.json.get('password')
    c.execute('select * from Employee where EmailAddress=? and Password=?', (email, password,))
    result = c.fetchone()
    conn.close()
    return jsonify(result)


# b)
@app.route('/search', methods=['get'])
def search_employee():
    searchText = request.json.get('search')
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute(
        "select * from Employee where EmployeeName like '%"+searchText+"%' or AccountName like '%"+searchText+"%' or EmailAddress like '%"+searchText+"%'"
    )
    result = c.fetchall()
    conn.close()
    return result


# c)
@app.route('/searchOrder/<id>', methods=['get'])
def search_order(id):
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    c.execute('select * from shopping where EmployeeID=?', (id,))
    result = c.fetchall()
    return jsonify(result)


# d)
@app.route('/importEmployee', methods=['post'])
def import_employee():
    data = request.get_json()
    conn = sqlite3.connect(sqldbname)
    c = conn.cursor()
    for employee in data['employees']:
        ename = employee['ename']
        aname = employee['aname']
        email = employee['email']
        password = employee['password']
        tel = employee['tel']
        department = employee['department']
        role = employee['role']
        c.execute(
            'insert into Employee (EmployeeName, AccountName, EmailAddress, Password, Tel, DepartmentID, RoleID) values (?,?,?,?,?,?,?)',
            (ename, aname, email, password, tel, department, role)
        )
        conn.commit()
    conn.close()
    return 'employee added'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
