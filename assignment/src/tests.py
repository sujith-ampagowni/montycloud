from unittest.mock import patch
from app import app

@patch('services.image_service.ImageService.get_presigned_upload_url')
def test_get_upload_url(mock_get_presigned_upload_url):
    mock_get_presigned_upload_url.return_value = ('http://test.com/upload', 'test-id')
    with app.test_client() as client:
        data = {'metadata': 'test metadata'}
        response = client.post('/upload', data=data)
        assert response.status_code == 200
        assert 'presigned_url' in response.json
        assert 'image_id' in response.json

@patch('services.image_service.ImageService.list_images')
def test_list_images(mock_list_images):
    mock_list_images.return_value = []
    with app.test_client() as client:
        response = client.get('/images')
        assert response.status_code == 200

@patch('services.image_service.ImageService.get_presigned_download_url')
def test_view_image(mock_get_presigned_download_url):
    mock_get_presigned_download_url.return_value = ('http://test.com/download', {'metadata': 'test'})
    with app.test_client() as client:
        response = client.get('/image/test-id')
        assert response.status_code == 200
        assert 'presigned_url' in response.json
        assert 'metadata' in response.json

@patch('services.image_service.ImageService.delete_image')
def test_delete_image(mock_delete_image):
    with app.test_client() as client:
        response = client.delete('/image/test-id')
        assert response.status_code == 200
