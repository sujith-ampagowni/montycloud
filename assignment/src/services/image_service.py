from services.s3_service import S3Service
import uuid


class ImageService:
    def __init__(self):
        self.s3_service = S3Service()

    def get_presigned_upload_url(self, metadata):
        image_id = str(uuid.uuid4())
        metadata['image_id'] = image_id
        presigned_url = self.s3_service.get_presigned_upload_url(image_id, metadata)
        return presigned_url

    def list_images(self, filter_key=None, filter_value=None):
        images = self.s3_service.list_images()
        if filter_key and filter_value:
            filtered_images = [img for img in images if img['Metadata'].get(filter_key) == filter_value]
            return filtered_images
        return images

    def get_presigned_download_url(self, image_id):
        return self.s3_service.get_presigned_download_url(image_id)

    def delete_image(self, image_id):
        self.s3_service.delete_image(image_id)