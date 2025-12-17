import yfinance as yf
from datetime import datetime
import schedule
import time
import os

# ============ CONFIGURACIÓN ============
# Ruta al escritorio (funciona en Windows, Mac y Linux)
ESCRITORIO = os.path.join(os.path.expanduser("~"), "Desktop")
NOMBRE_ARCHIVO = "datos_bolsa.txt"
RUTA_ARCHIVO = os.path.join(ESCRITORIO, NOMBRE_ARCHIVO)

# Símbolos de las acciones
ATRESMEDIA = "A3M.MC"  # Atresmedia en la bolsa española
IBEX35 = "^IBEX"       # IBEX 35

def obtener_datos_bolsa():
    """Obtiene los datos actuales de la bolsa"""
    datos = {}
    
    try:
        # Obtener datos de Atresmedia
        atresmedia = yf.Ticker(ATRESMEDIA)
        info_atresmedia = atresmedia.info
        hist_atresmedia = atresmedia.history(period="1d")
        
        if not hist_atresmedia.empty:
            datos['atresmedia'] = {
                'nombre': info_atresmedia.get('longName', 'Atresmedia'),
                'precio_actual': hist_atresmedia['Close'].iloc[-1],
                'precio_apertura': hist_atresmedia['Open'].iloc[-1],
                'precio_maximo': hist_atresmedia['High'].iloc[-1],
                'precio_minimo': hist_atresmedia['Low'].iloc[-1],
                'volumen': hist_atresmedia['Volume'].iloc[-1],
            }
            
            # Calcular cambio
            cambio = hist_atresmedia['Close'].iloc[-1] - hist_atresmedia['Open'].iloc[-1]
            cambio_porcentual = (cambio / hist_atresmedia['Open'].iloc[-1]) * 100
            datos['atresmedia']['cambio'] = cambio
            datos['atresmedia']['cambio_porcentual'] = cambio_porcentual
        
        # Obtener datos del IBEX 35
        ibex = yf.Ticker(IBEX35)
        hist_ibex = ibex.history(period="1d")
        
        if not hist_ibex.empty:
            datos['ibex35'] = {
                'nombre': 'IBEX 35',
                'precio_actual': hist_ibex['Close'].iloc[-1],
                'precio_apertura': hist_ibex['Open'].iloc[-1],
                'precio_maximo': hist_ibex['High'].iloc[-1],
                'precio_minimo': hist_ibex['Low'].iloc[-1],
                'volumen': hist_ibex['Volume'].iloc[-1],
            }
            
            cambio = hist_ibex['Close'].iloc[-1] - hist_ibex['Open'].iloc[-1]
            cambio_porcentual = (cambio / hist_ibex['Open'].iloc[-1]) * 100
            datos['ibex35']['cambio'] = cambio
            datos['ibex35']['cambio_porcentual'] = cambio_porcentual
            
    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")
        return None
    
    return datos

def crear_texto_bonito(datos):
    """Crea el texto formateado para el archivo"""
    fecha_hora = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    
    texto = f"""
{'='*70}
                    📊 RESUMEN DE BOLSA
{'='*70}
Fecha y Hora: {fecha_hora}
{'='*70}

🏢 ATRESMEDIA (A3M.MC)
{'─'*70}
  Precio Actual:       {datos['atresmedia']['precio_actual']:.2f} €
  Precio Apertura:     {datos['atresmedia']['precio_apertura']:.2f} €
  Precio Máximo:       {datos['atresmedia']['precio_maximo']:.2f} €
  Precio Mínimo:       {datos['atresmedia']['precio_minimo']:.2f} €
  
  Cambio del día:      {datos['atresmedia']['cambio']:+.2f} € ({datos['atresmedia']['cambio_porcentual']:+.2f}%)
  {'📈 SUBIDA' if datos['atresmedia']['cambio'] >= 0 else '📉 BAJADA'}
  
  Volumen:             {datos['atresmedia']['volumen']:,.0f} acciones

{'='*70}

📈 IBEX 35
{'─'*70}
  Precio Actual:       {datos['ibex35']['precio_actual']:.2f}
  Precio Apertura:     {datos['ibex35']['precio_apertura']:.2f}
  Precio Máximo:       {datos['ibex35']['precio_maximo']:.2f}
  Precio Mínimo:       {datos['ibex35']['precio_minimo']:.2f}
  
  Cambio del día:      {datos['ibex35']['cambio']:+.2f} ({datos['ibex35']['cambio_porcentual']:+.2f}%)
  {'📈 SUBIDA' if datos['ibex35']['cambio'] >= 0 else '📉 BAJADA'}
  
  Volumen:             {datos['ibex35']['volumen']:,.0f}

{'='*70}


"""
    return texto

def guardar_en_archivo(datos):
    """Guarda o añade los datos al archivo en el escritorio"""
    try:
        texto = crear_texto_bonito(datos)
        
        # Modo 'a' para añadir al final del archivo (append)
        # Si quieres sobrescribir cada vez, usa 'w' en lugar de 'a'
        with open(RUTA_ARCHIVO, 'a', encoding='utf-8') as archivo:
            archivo.write(texto)
        
        print(f"✅ Datos guardados correctamente en: {RUTA_ARCHIVO}")
        print(f"   Hora: {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error al guardar archivo: {e}")

def tarea_diaria():
    """Función que se ejecuta diariamente"""
    print(f"\n🔄 Ejecutando tarea a las {datetime.now().strftime('%H:%M:%S')}")
    
    datos = obtener_datos_bolsa()
    
    if datos:
        guardar_en_archivo(datos)
    else:
        print("❌ No se pudieron obtener los datos de la bolsa")

# Programar la tarea diaria a las 21:00
schedule.every().day.at("21:00").do(tarea_diaria)

if __name__ == "__main__":
    print("🚀 Script de bolsa iniciado")
    print(f"📁 Archivo se guardará en: {RUTA_ARCHIVO}")
    print("⏰ El script guardará datos diariamente a las 21:00")
    print("💡 Presiona Ctrl+C para detener el script\n")
    
    # Ejecutar inmediatamente para probar
    print("🧪 Ejecutando prueba inmediata...")
    tarea_diaria()
    
    # Bucle infinito para mantener el script corriendo
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verifica cada minuto