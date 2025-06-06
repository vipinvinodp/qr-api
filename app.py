from flask import Flask, request, send_file, jsonify
import qrcode
from PIL import Image
import json
import io

app = Flask(__name__)

# Load logo (doll image) once
logo_path = "doll.png"
logo = Image.open(logo_path)
logo_size = 100
logo.thumbnail((logo_size, logo_size))

@app.route("/generate_qr", methods=["GET"])
def generate_qr():
    try:
        # Collect query parameters
        X1 = request.args.get("X1", "")
        X2 = request.args.get("X2", "")
        X3 = request.args.get("X3", "")
        X4a = request.args.get("X4a", "")
        X4b = request.args.get("X4b", "")
        X5 = request.args.get("X5", "")

        # Structure the JSON data
        data = {
            "X1": X1,
            "X2": X2,
            "X3": X3,
            "X4": [X4a, X4b],
            "X5": X5
        }

        qr_content = json.dumps(data, separators=(',', ':'))

        # Generate QR
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Add logo to center
        qr_width, qr_height = img_qr.size
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        img_qr.paste(logo, logo_pos, mask=logo if logo.mode == 'RGBA' else None)

        # Save image to memory
        img_io = io.BytesIO()
        img_qr.save(img_io, format='PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
