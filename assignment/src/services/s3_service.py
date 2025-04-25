import boto3

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client('s3', endpoint_url='http://localhost:4566', region_name='us-east-1')
        self.bucket_name = 'my-instagram-bucket'

    def get_presigned_upload_url(self, image_id, metadata):
        return self.s3_client.generate_presigned_url('put_object',
                                                     Params={'Bucket': self.bucket_name,
                                                             'Key': image_id, 'Metadata': metadata},
                                                     ExpiresIn=3600)

    def get_presigned_download_url(self, image_id):
        url = self.s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': self.bucket_name, 'Key': image_id},
                                                    ExpiresIn=3600)
        response = self.s3_client.head_object(Bucket=self.bucket_name, Key=image_id)
        metadata = response['Metadata']
        return url, metadata

    def delete_image(self, image_id):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=image_id)
