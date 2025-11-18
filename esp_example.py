import paho.mqtt.client as mqtt
import requests
import threading
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "api_vision/spot/03"

last_image = None  # guarda a última imagem enviada

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao MQTT!")
        client.subscribe(TOPIC)
    else:
        print("Erro ao conectar:", rc)

def on_message(client, userdata, msg):
    global last_image

    payload = msg.payload.decode()
    print(f"Mensagem recebida: {payload}")

    if "take_picture" in payload:
        print("Comando take_picture recebido!")

        # Alternância correta
        if last_image == "teste_image.png":
            choice_image = "teste_image2.png"
        else:
            choice_image = "teste_image.png"

        last_image = choice_image

        print(f"Imagem enviada: {choice_image}")

        response = requests.post(
            "http://localhost:8000/api/plate/validate/",
            files={"file": open(choice_image, "rb")},
            data={"id": "03", "status": "OCUPADO"}
        )

        print("Resposta:", response.status_code, response.text)

# --------------------------
# LOOP AUTOMÁTICO DE 15s 
# --------------------------
def auto_publish():
    while True:
        time.sleep(15)
        print("⏱️ Enviando comando take_picture automaticamente...")
        client.publish(TOPIC, "take_picture")

# --------------------------
# MQTT CLIENT
# --------------------------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

# inicia thread paralela
threading.Thread(target=auto_publish, daemon=True).start()

client.loop_forever()
