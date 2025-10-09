import numpy as np
import matplotlib.pyplot as plt

def crecimiento_exponencial(P0, r, t):
    """
    Calcula el crecimiento exponencial
    P0: Población inicial
    r: Tasa de crecimiento
    t: Tiempo
    """
    tiempo = np.arange(t + 1)
    poblacion = P0 * np.exp(r * tiempo)
    
    return tiempo, poblacion

def graficar_crecimiento_exponencial(P0, r, t):
    tiempo, poblacion = crecimiento_exponencial(P0, r, t)
    
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, poblacion, 'b-', linewidth=2, label=f'P0={P0}, r={r}')
    plt.title('Modelo de Crecimiento Exponencial')
    plt.xlabel('Tiempo')
    plt.ylabel('Población')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Guardar imagen
    plt.savefig('images/crec_exponencial.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return tiempo, poblacion

# Ejemplo de uso
if __name__ == "__main__":
    # Parámetros: P0=100, r=0.1, t=50
    tiempo, poblacion = graficar_crecimiento_exponencial(100, 0.1, 50)
    print("Crecimiento Exponencial:")
    for t, p in zip(tiempo[::5], poblacion[::5]):
        print(f"t={t}: P(t)={p:.2f}")