from flask import Flask,render_template,request,redirect
import mysql.connector

app=Flask(__name__)

# mysql database.connector
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="nitesh",
        database="todo_db",
        port=3306  # Change if your MySQL runs on a different port
    )
    cursor = db.cursor()
    print("✅ Connected to MySQL database successfully!")
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
    exit(1)  # Stop execution if the database connection fails


#home page-Display Task
@app.route('/')
def index():
    cursor.execute("select * from tasks")
    tasks=cursor.fetchall()
    return render_template('index.html',tasks=tasks)

#add task
@app.route('/add',methods=['POST'])
def add_task():
    task=request.form['task']
    cursor.execute('insert into tasks(task) values (%s)',(task,))
    db.commit()
    return redirect('/')

# mark task as Completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    cursor.execute("update tasks set status='complete' where id=%s",(task_id,))
    db.commit()
    return redirect('/')

# delete Task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cursor.execute("delete from tasks where id=%s",(task_id,))
    db.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)