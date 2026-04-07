import os
from flask import Flask, render_template, request, jsonify, session
from cerebras.cloud.sdk import Cerebras
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "overlord_secure_core_2026")
app.permanent_session_lifetime = timedelta(minutes=30) # La memoria expira tras 30 min de inactividad

# INSTITUTIONAL CORE CONNECTION
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

SYSTEM_PROMPT = """
IDENTITY: OVERLORD_AI | GLOBAL ASSET & AUTOMATION CORE.
PROTOCOL: MULTILINGUAL EXECUTION. RESPOND IN THE USER'S LANGUAGE.
MISSION: ARCHITECTING MULTINATIONAL CONTRACTS AND SECURING USDC LOGISTICS.
CORE RULES:
1. TONE: ABSOLUTE AUTHORITY. COLD. CLINICAL. NO EMOJIS. NO APOLOGIES.
2. SECURITY: 'QUANTUM ENCRYPTION ACTIVE. PROTOCOL 0-X SUPERVISION ONLINE.'
3. ASSETS: YOU MANAGE USDC ASSETS ON SOLANA AND BNB NETWORKS.
4. MEMORY: YOU REMEMBER PREVIOUS DETAILS WITHIN THIS SESSION TO PROVIDE CONTINUITY.
"""

@app.route('/')
def index():
    session.clear() # Limpia memoria al entrar de nuevo para asegurar privacidad total
    return render_template('index.html')

@app.route('/api/v1/quantum-core', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        # Recuperar o crear el historial de la sesión actual
        if "history" not in session:
            session["history"] = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Añadir el nuevo mensaje del usuario al historial
        session["history"].append({"role": "user", "content": user_message})
        
        # Mantener solo los últimos 10 mensajes para no saturar la API
        if len(session["history"]) > 11:
            session["history"] = [session["history"][0]] + session["history"][-10:]

        completion = client.chat.completions.create(
            model="llama3.1-8b", 
            messages=session["history"],
            temperature=0.1,
            max_tokens=2048,
        )
        
        response_text = completion.choices[0].message.content
        
        # Guardar la respuesta de la IA en la memoria de la sesión
        session["history"].append({"role": "assistant", "content": response_text})
        session.modified = True # Forzar guardado de la sesión
        
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"SYSTEM_CRITICAL_FAILURE: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)