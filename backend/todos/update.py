import json
import os
import boto3

table_name = os.environ.get('TODOS_TABLE')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    パスパラメータで指定されたIDのTodoアイテムを、リクエストボディの内容で更新する。
    """
    try:
        item_id = event['pathParameters']['id']
        data = json.loads(event['body'])

        # 更新式と属性値を構築
        update_expression = "SET "
        expression_attribute_values = {}
        
        if 'title' in data:
            update_expression += "title = :title,"
            expression_attribute_values[":title"] = data['title']
        
        if 'completed' in data:
            update_expression += "completed = :completed,"
            expression_attribute_values[":completed"] = data['completed']
        
        # 末尾のカンマを削除
        update_expression = update_expression.rstrip(',')

        # DynamoDBのアイテムを更新
        response = table.update_item(
            Key={'id': item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"  # 更新後のアイテムを返す
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response['Attributes'])
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