from flask import Flask, request
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from apex import extract_data
import requests
import camelot
import os
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Extract(Resource):
    def get(self):
        return {'about': 'Hello World'}

    def post(self):
        url = request.args.get('url')

        table = camelot.read_pdf(url)
        if len(table) == 0:
            return 'No table was Detected'
        stuffs = table[0].df
        stuffs.drop([0], inplace=True)
        stuffs.columns = ['s/n', 'customer_name', 'amount', 'rate',
                          'item_of_import', 'form_m_number', 'bank_name']
        informations = []

        for index, row in stuffs.iterrows():

            print(len(stuffs))

            endpoint = 'https://trkew0yekahyonq-tradefin.adb.uk-london-1.oraclecloudapps.com/ords/tradefin/dump/store'
            element = {'customer_name': row['customer_name'],
                       'amount': row['amount'].replace(',', ''),
                       'rate': row['rate'],
                       'item_of_import': row['item_of_import'],
                       'form_m_number': row['form_m_number'],
                       'bank_name': row['bank_name'],
                       'value_date': '3/4/2019'
                       }
            print('Saving to database...')
            informations.append(element)
            r = requests.post(url=endpoint, data=element)
        #     print(element['amount'])
            # print(r.status_code)
            # return informations
        return "Number of Customers Extracted", len(stuffs), {'Extracted Details': informations}, 201


class Give(Resource):
    def get(self, num):
        return {'result': num*10}


api.add_resource(Extract, '/')
api.add_resource(Give, '/give/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)
