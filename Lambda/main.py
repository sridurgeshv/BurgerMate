from flask import Flask, jsonify
import boto3

app = Flask(__name__)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

@app.route('/getOrders', methods=['GET'])
def get_orders():
    try:
        # Scan the DynamoDB table to get all orders
        response = table.scan()
        orders = response.get('Items', [])
        return jsonify(orders), 200
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return jsonify({'error': 'Unable to fetch orders'}), 500

if __name__ == '__main__':
    app.run(debug=True)
