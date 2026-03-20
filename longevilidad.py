import sys
import os

# 1. Forzamos la ruta local para que encuentre Bio y requests
sys.path.append(os.path.join(os.getcwd(), ".venv", "Lib", "site-packages"))

try:
    import requests
    from Bio import Entrez, SeqIO
    print("[+] SISTEMA CONECTADO: Librerías detectadas correctamente.")
except ImportError:
    print("[-] ERROR: Aún no se detectan las librerías en .venv")

Entrez.email = "tu_correo@ejemplo.com"

def verificar_capital_usdc():
    # Esto es lo que te dará la libertad para viajar
    print("\n--- CONSULTANDO PRECIO DE MERCADO (USDC/BTC) ---")
    try:
        r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=10)
        precio = r.json()['bpi']['USD']['rate']
        print(f"[EXITO]: Valor actual para tus ahorros: ${precio} USD")
    except:
        print("[-] Error de red. Revisa tu conexión a internet.")

def analizar_dsup_tardigrado():
    # Bio-ingeniería para tu portafolio internacional
    print("\n--- ANALIZANDO PROTEÍNA DE RESISTENCIA DSUP ---")
    try:
        handle = Entrez.efetch(db="nucleotide", id="LC012555.1", rettype="fasta", retmode="text")
        record = SeqIO.read(handle, "fasta")
        gc = (record.seq.count("G") + record.seq.count("C")) / len(record.seq) * 100
        print(f"[DNA]: Estabilidad detectada: {gc:.2f}%")
        print(f"[DNA]: Genoma: {record.description[:60]}...")
    except Exception as e:
        print(f"[-] Error en base de datos NCBI: {e}")

if __name__ == "__main__":
    verificar_capital_usdc()
    analizar_dsup_tardigrado()