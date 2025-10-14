import json
import os
import boto3

table_name = os.environ.get('TODOS_TABLE')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    パスパラメータで指定されたIDのTodoアイテムをDynamoDBから取得する。
    """
    try:
        # パスパラメータからIDを取得
        item_id = event['pathParameters']['id']
        
        # DynamoDBからアイテムを取得
        response = table.get_item(Key={'id': item_id})
        
        # アイテムが存在するかチェック
        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404, # 404 Not Found
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Item not found'})
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