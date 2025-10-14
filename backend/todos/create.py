import json
import os
import uuid
import boto3
from datetime import datetime

# 環境変数からテーブル名を取得
table_name = os.environ.get('TODOS_TABLE')
# DynamoDBリソースを取得
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    API GatewayからのPOSTリクエストを受け取り、新しいTodoアイテムをDynamoDBに保存する。
    """
    try:
        # リクエストボディをJSONとしてパース
        data = json.loads(event['body'])

        # 必須フィールドの存在チェック
        if 'title' not in data:
            raise ValueError("リクエストボディに'title'フィールドが必要です。")

        # 保存するアイテムを作成
        item = {
            'id': str(uuid.uuid4()),  # ユニークなIDを生成
            'title': data['title'],
            'completed': False,  # デフォルトは未完了
            'createdAt': datetime.utcnow().isoformat() + "Z"  # ISO 8601形式のUTCタイムスタンプ
        }

        # DynamoDBにアイテムを書き込む
        table.put_item(Item=item)

        # 成功レスポンスを返す
        return {
            'statusCode': 201, # 201 Created
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # CORS対応
            },
            'body': json.dumps(item)
        }
    
    except Exception as e:
        # エラーハンドリング
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }