from flask import Flask, render_template, request

app=Flask(__name__)



@app.route('/')
def inicial():
    return render_template('index.html')
   


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registrar')
def registrar():
    return render_template('registrar.html')
   



if __name__ == '__main__':
    app.run(debug=True)