import json
import os
import boto3

table_name = os.environ.get('TODOS_TABLE')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    パスパラメータで指定されたIDのTodoアイテムをDynamoDBから削除する。
    """
    try:
        item_id = event['pathParameters']['id']
        
        # DynamoDBからアイテムを削除
        table.delete_item(Key={'id': item_id})
        
        return {
            'statusCode': 204, # 204 No Content
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': ""
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }