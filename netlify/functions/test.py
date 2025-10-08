def handler(event, context):
    """Simple test function"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': '{"message": "Netlify Functions are working!", "timestamp": "' + str(context.aws_request_id) + '"}'
    }
