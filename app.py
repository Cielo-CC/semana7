from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/exponencial')
def exponencial():
    return render_template('pages/exponencial.html')

@app.route('/logistico')
def logistico():
    return render_template('pages/logistico.html')

@app.route('/calcular_exponencial', methods=['POST'])
def calcular_exponencial():
    data = request.json
    P0 = float(data['P0'])
    r = float(data['r'])
    t = int(data['t'])
    
    # Cálculo del crecimiento exponencial
    tiempo = np.arange(t + 1)
    poblacion = P0 * np.exp(r * tiempo)
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, poblacion, 'b-', linewidth=2)
    plt.title('Crecimiento Exponencial')
    plt.xlabel('Tiempo')
    plt.ylabel('Población')
    plt.grid(True)
    
    # Convertir gráfico a base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return jsonify({
        'tiempo': tiempo.tolist(),
        'poblacion': poblacion.tolist(),
        'grafico': plot_url
    })

if __name__ == '__main__':
    app.run(debug=True)