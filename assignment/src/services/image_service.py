from services.s3_service import S3Service
from services.dynamodb_service import DynamoDBService
import uuid

class ImageService:
    def __init__(self):
        self.s3_service = S3Service()
        self.dynamodb_service = DynamoDBService()

    def get_presigned_upload_url(self, metadata):
        image_id = str(uuid.uuid4())
        metadata['image_id'] = image_id
        metadata['s3_path'] = f's3://{self.s3_service.bucket_name}/{image_id}'
        presigned_url = self.s3_service.get_presigned_upload_url(image_id, metadata)
        self.dynamodb_service.store_metadata(metadata)
        return presigned_url, image_id

    def list_images(self, filters):
        return self.dynamodb_service.list_images(filters)

    def get_presigned_download_url(self, image_id):
        return self.s3_service.get_presigned_download_url(image_id)

    def delete_image(self, image_id):
        self.s3_service.delete_image(image_id)
        self.dynamodb_service.delete_metadata(image_id)