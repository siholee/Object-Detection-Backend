from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)

# Load your custom YOLOv8 model (assuming the model file is located in 'models/logishub.pt')
model = YOLO('models/logishub.pt')

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        results = model(image)

        # Extract detection results, filtering only classes learned by the custom model
        counts = {}

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]  # Get class name using model's names property
                counts[class_name] = counts.get(class_name, 0) + 1

        return jsonify({'detections': counts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)