from flask import Flask, render_template

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



@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')


@app.route('/redefinir')
def redefinir():
    return render_template('redefinir.html')


@app.route('/codigo')
def codigo():
    return render_template('codigo.html')
   



if __name__ == '__main__':
    app.run(debug=True)