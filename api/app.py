from flask import Flask, request
from flask import render_template
import importlib.machinery
loader = importlib.machinery.SourceFileLoader('api', 'agent/app.py')
h = loader.load_module('api')

app = Flask(__name__)

@app.route('/')
def todo():
    resultado=h.listarMonedas()
    return render_template('todo.html', datos=resultado)

@app.route('/cargarMonedas')
def cargarMonedas():
    h.guardarMonedas()
    resultado=h.listarMonedas()
    return render_template('todo.html', datos=resultado)

@app.route('/verTodaInformacion', methods=["POST"])
def verTodaInformacion():
    if request.method == 'POST':
        name = request.form['name']
        rank = request.form['rank']
    check=h.chequearDatos(rank)
    if (check==True):
        resultado=h.buscarMoneda(name)
        return render_template('mostrarMoneda.html', datos=resultado)
    else:
        return render_template('error.html')

@app.route('/verTop5')
def verTop5():
    resultado=h.top5()
    return render_template('verTop5.html', datos=resultado)

@app.route('/verTop20')
def verTop20():
    resultado=h.top20()
    return render_template('verTop20.html', datos=resultado)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)