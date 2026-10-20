from pathlib import Path
import json

import cv2
import face_recognition
import numpy as np
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024

REGISTRATION_FILE = Path(__file__).resolve().with_name("cadastro_facial.json")
MATCH_TOLERANCE = 0.50
FRAME_SCALE = 0.5

app.reference_encoding = None
app.registered_name = None


def read_uploaded_frame():
    """Lê um frame JPEG enviado pelo navegador e o converte para RGB."""
    uploaded_frame = request.files.get("frame")
    if uploaded_frame is None:
        raise ValueError("O frame da webcam não foi enviado.")

    image_bytes = np.frombuffer(uploaded_frame.read(), dtype=np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Não foi possível ler a imagem capturada pela webcam.")

    small_frame = cv2.resize(frame, (0, 0), fx=FRAME_SCALE, fy=FRAME_SCALE)
    return cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)


def load_registration():
    """Carrega o encoding salvo localmente, caso já exista um cadastro."""
    if not REGISTRATION_FILE.is_file():
        return None, None

    try:
        registration = json.loads(REGISTRATION_FILE.read_text(encoding="utf-8"))
        encoding = np.asarray(registration["encoding"], dtype=np.float64)
        name = registration["name"].strip()
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        raise RuntimeError(
            f"Não foi possível ler o cadastro salvo: {error}"
        ) from error

    if encoding.shape != (128,) or not np.isfinite(encoding).all() or not name:
        raise RuntimeError(
            "O cadastro salvo está inválido. Faça o cadastro novamente."
        )
    return encoding, name


@app.get("/")
def index():
    return render_template(
        "index.html",
        registered_name=app.registered_name,
    )


@app.post("/api/register")
def register_face():
    name = request.form.get("name", "").strip()
    if not name:
        return jsonify(error="Digite o nome da pessoa antes de cadastrar."), 400
    if len(name) > 60:
        return jsonify(error="O nome deve ter no máximo 60 caracteres."), 400

    try:
        rgb_frame = read_uploaded_frame()
    except ValueError as error:
        return jsonify(error=str(error)), 400

    locations = face_recognition.face_locations(rgb_frame)
    if not locations:
        return jsonify(error="Nenhum rosto foi encontrado. Olhe para a câmera e tente novamente."), 400
    if len(locations) > 1:
        return jsonify(error="Foi encontrado mais de um rosto. Deixe apenas uma pessoa na imagem."), 400

    encodings = face_recognition.face_encodings(rgb_frame, locations)
    if not encodings:
        return jsonify(error="Não foi possível cadastrar esse rosto. Tente com mais iluminação."), 400

    try:
        temporary_file = REGISTRATION_FILE.with_suffix(".tmp")
        temporary_file.write_text(
            json.dumps(
                {"name": name, "encoding": encodings[0].tolist()},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        temporary_file.replace(REGISTRATION_FILE)
    except OSError as error:
        return jsonify(error=f"Não foi possível salvar o cadastro: {error}"), 500

    app.reference_encoding = encodings[0]
    app.registered_name = name
    return jsonify(
        message=f"Cadastro realizado! Rosto reconhecido: {name}.",
        registered_name=name,
    )


@app.post("/api/recognize")
def recognize():
    if app.reference_encoding is None:
        return jsonify(error="Cadastre um rosto antes de iniciar o reconhecimento."), 409

    try:
        rgb_frame = read_uploaded_frame()
    except ValueError as error:
        return jsonify(error=str(error)), 400

    locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, locations)
    faces = []

    for (top, right, bottom, left), encoding in zip(locations, encodings):
        distance = float(
            face_recognition.face_distance(
                [app.reference_encoding], encoding
            )[0]
        )
        matched = distance <= MATCH_TOLERANCE
        faces.append(
            {
                "box": {
                    "top": round(top / FRAME_SCALE),
                    "right": round(right / FRAME_SCALE),
                    "bottom": round(bottom / FRAME_SCALE),
                    "left": round(left / FRAME_SCALE),
                },
                "matched": matched,
                "name": app.registered_name if matched else "Desconhecido",
            }
        )

    return jsonify(
        faces=faces,
        access_granted=any(face["matched"] for face in faces),
        width=rgb_frame.shape[1] / FRAME_SCALE,
        height=rgb_frame.shape[0] / FRAME_SCALE,
    )


def main():
    try:
        app.reference_encoding, app.registered_name = load_registration()
    except RuntimeError as error:
        print(f"Aviso: {error}")
        print("O site abrirá; faça um novo cadastro pelo navegador.")

    print("Site iniciado em http://127.0.0.1:5000")
    print("Deixe este terminal aberto enquanto usa o site.")
    app.run(host="127.0.0.1", port=5000, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
