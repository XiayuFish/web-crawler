# cd C:\AIiot\Report\gapminder-api   

import flask
from flask import jsonify, request
import pandas as pd
import numpy as np

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello gogo</h1>"
    

# test data
# paper = {
#     "id": 0,
#     "product": "衛生紙",
#     "price": "415",
#     "category": "日用品"   
# }
# wash = {
#     "id": 1,
#     "product": "洗面乳",
#     "price": "199",
#     "category": "美妝"    
# }
# coffee = {
#     "id": 2,
#     "product": "周末咖啡",
#     "price": "148",
#     "category": "咖啡、茶包"    
# }
# products = [paper, wash, coffee]

# @app.route('/products', methods=['GET'])
# def products_all():
#     return jsonify(products)

data0125 = pd.read_csv("data0125.csv")
data0125_list = []
nrows = data0125.shape[0] #shape[0]返回的是二維陣列的列數。

for i in range(nrows):
    ser = data0125.loc[i, :] #loc[“索引名稱”, “欄位名稱”] :表全部
    row_dict = {}
    for idx, val in zip(ser.index, ser.values):
        if type(val) is str:
            row_dict[idx] = val
        elif type(val) is np.int64:
            row_dict[idx] = int(val)
        elif type(val) is np.float64:
            row_dict[idx] = float(val)
    data0125_list.append(row_dict)

@app.route('/data0125', methods=['GET'])
def product_data():
    return jsonify(data0125_list)
    
# @app.route('/products_data', methods=['GET'])
# def product():
#     if 'product' in request.args:
#         product = request.args['product']
#     else:
#         return "Error: No product provided. Please specify a product."
#     results = []

#     for city in cities:
#         if city['product'] == product:
#             results.append(city)

#     return jsonify(results)



# @app.route('/data0125', methods=['GET'])
# def country():
#     if 'country' in request.args:
#         country = request.args['country']
#     else:
#         return "Error: No country provided. Please specify a country."
#     results = []

#     for elem in data0125_list:
#         if elem['country'] == country:
#             results.append(elem)

#     return jsonify(results)

app.run()
