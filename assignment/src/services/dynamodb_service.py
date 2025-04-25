import boto3

class DynamoDBService:
    def __init__(self):
        self.dynamodb_client = boto3.client('dynamodb', endpoint_url='http://localhost:4566', region_name='us-east-1')
        self.table_name = 'ImageMetadata'

    def store_metadata(self, metadata):
        self.dynamodb_client.put_item(TableName=self.table_name, Item={k: {'S': v} for k, v in metadata.items()})

    def list_images(self, filters):
        scan_kwargs = {}
        if filters:
            filter_expressions = []
            expression_attribute_values = {}
            for key, value in filters.items():
                filter_expressions.append(f'{key} = :{key}')
                expression_attribute_values[f':{key}'] = {'S': value}
            scan_kwargs = {
                'FilterExpression': ' AND '.join(filter_expressions),
                'ExpressionAttributeValues': expression_attribute_values
            }
        response = self.dynamodb_client.scan(TableName=self.table_name, **scan_kwargs)
        return response.get('Items', [])

    def delete_metadata(self, image_id):
        self.dynamodb_client.delete_item(TableName=self.table_name, Key={'image_id': {'S': image_id}})