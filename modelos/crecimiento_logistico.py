import numpy as np
import matplotlib.pyplot as plt

def crecimiento_logistico(P0, r, K, t):
    """
    Calcula el crecimiento logístico
    P0: Población inicial
    r: Tasa de crecimiento
    K: Capacidad de carga
    t: Tiempo
    """
    tiempo = np.arange(t + 1)
    poblacion = K / (1 + ((K - P0) / P0) * np.exp(-r * tiempo))
    
    return tiempo, poblacion

def graficar_crecimiento_logistico(P0, r, K, t):
    tiempo, poblacion = crecimiento_logistico(P0, r, K, t)
    
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, poblacion, 'r-', linewidth=2, label=f'P0={P0}, r={r}, K={K}')
    plt.axhline(y=K, color='g', linestyle='--', alpha=0.7, label=f'Capacidad de carga (K={K})')
    plt.title('Modelo de Crecimiento Logístico')
    plt.xlabel('Tiempo')
    plt.ylabel('Población')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Guardar imagen
    plt.savefig('images/crec_logistico.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return tiempo, poblacion

# Ejemplo de uso
if __name__ == "__main__":
    # Parámetros: P0=10, r=0.2, K=1000, t=100
    tiempo, poblacion = graficar_crecimiento_logistico(10, 0.2, 1000, 100)
    print("Crecimiento Logístico:")
    for t, p in zip(tiempo[::10], poblacion[::10]):
        print(f"t={t}: P(t)={p:.2f}")