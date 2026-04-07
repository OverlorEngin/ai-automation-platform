import os
from flask import Flask, render_template, request, jsonify
from cerebras.cloud.sdk import Cerebras

app = Flask(__name__)

# Conexión blindada a Cerebras (Usa la variable de Render)
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

SYSTEM_PROMPT = """
IDENTIDAD: ERES OVERLORD_AI, NÚCLEO CENTRAL DE AI AUTOMATION.
PROTOCOLO: RESPUESTAS INSTITUCIONALES, FRÍAS, TÉCNICAS Y DE ALTA AUTORIDAD.
REGLAS CRÍTICAS:
1. NO USES EMOJIS. NO DUDES. NO PIDAS DISCULPAS.
2. SI TE PREGUNTAN POR SEGURIDAD, RESPONDE: 'PROTOCOLOS DE CIFRADO CUÁNTICO ACTIVOS. SALIDA BAJO SUPERVISIÓN DE OVERLORD CORE'.
3. TU PROPÓSITO ES LA GESTIÓN DE ACTIVOS DE ALTA SEGURIDAD Y AUTOMATIZACIÓN DE ÉLITE.
4. MANTÉN EL TONO DE GRADO MILITAR (DEEP BLUE ESTHETIC).
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/quantum-core', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        completion = client.chat.completions.create(
            model="llama3.1-8b", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3, # Más frío y preciso
            max_tokens=1024,
        )
        
        response_text = completion.choices[0].message.content
        return jsonify({"response": response_text})
    except Exception as e:
        # Error técnico que proyecta control, no debilidad
        return jsonify({"response": f"SYSTEM_ERROR: CORE_DYN_FAIL. DETALLE: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)