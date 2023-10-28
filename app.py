from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1Horntail!'
app.config['MYSQL_DB'] = 'recipes'

mysql = MySQL(app)

#Homepage
@app.route('/', methods = ["GET"])
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recipe_info WHERE category = 'BreakFast'")
    BreakFast = cur.fetchall()
    cur.execute("SELECT * FROM recipe_info WHERE category = 'Lunch'")
    Lunch = cur.fetchall()
    cur.execute("SELECT * FROM recipe_info WHERE category = 'Dinner'")
    Dinner = cur.fetchall()
    cur.execute("SELECT * FROM recipe_info WHERE category = 'Dessert'")
    Dessert = cur.fetchall()
    print(Dessert)
    print(Dinner)
    print(Lunch)
    print(BreakFast)
    cur.close()
    return render_template('home.html', BreakFast = BreakFast, Lunch=Lunch, Dinner=Dinner, Dessert = Dessert)

#Add recipe
@app.route('/addrecipe', methods = ["GET", "POST"])
def addrecipe():
    if request.method == "POST":
       name = request.form['recipe_name']
       category = request.form['category']
       ingredient = request.form['ingredient']
       cur = mysql.connection.cursor()
       cur.execute("INSERT INTO recipe_info(recipe_name, category, ingredient) VALUES(%s,%s,%s)", (name, category, ingredient))
       mysql.connection.commit()
       cur.close()
       return redirect(url_for ("home"))
    
    return render_template('addrecipe.html')

#Edit Recipe
@app.route("/editrecipe/<int:id>", methods=["GET", "POST"])
def update(id):
    print(id)
    cur = mysql.connection.cursor()
    if request.method=="POST":
        name = request.form['recipe_name']
        category = request.form['category']
        ingredient = request.form['ingredient']
        cur.execute("UPDATE recipe_info SET recipe_name = %s, category = %s, ingredient = %s WHERE id=%s",( name, category, ingredient,id))
        mysql.connection.commit()
        mysql.connection.close
        return redirect(url_for ("home"))
    cur.execute("SELECT * FROM recipe_info WHERE id = %s", (id,))
    info = cur.fetchall()
    print(info)
    return render_template('editrecipe.html', info=info)

#Delete recipe
@app.route("/delete/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()                                 
    cur.execute('DELETE FROM recipe_info WHERE id = %s', (id,))     
    mysql.connection.commit()                                       
    return redirect(url_for('home'))   


app.run(debug=True)