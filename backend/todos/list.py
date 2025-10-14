import json
import os
import boto3

table_name = os.environ.get('TODOS_TABLE')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    DynamoDBテーブルから全てのTodoアイテムを取得して返す。
    """
    try:
        # テーブル全体をスキャンしてアイテムを取得
        response = table.scan()
        
        # 成功レスポンスを返す
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response.get('Items', []))
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
