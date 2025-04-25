from flask import Flask, request, jsonify
from services.image_service import ImageService

app = Flask(__name__)
image_service = ImageService()

@app.route('/upload', methods=['POST'])
def get_upload_url():
    try:
        metadata = request.form.to_dict()
        presigned_url, image_id = image_service.get_presigned_upload_url(metadata)
        return jsonify({'presigned_url': presigned_url, 'image_id': image_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/images', methods=['GET'])
def list_images():
    try:
        filters = request.args.to_dict()
        images = image_service.list_images(filters)
        return jsonify(images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/image/<image_id>', methods=['GET'])
def view_image(image_id):
    try:
        presigned_url, metadata = image_service.get_presigned_download_url(image_id)
        return jsonify({'presigned_url': presigned_url, 'metadata': metadata}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/image/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    try:
        image_service.delete_image(image_id)
        return jsonify({'message': 'Image deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
