from django.db import models
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional

# Create your models here.
class Transaction:
    """
    Transaction Class to Management the Query Filter on MongoDB
    """

    @staticmethod
    def result(type: str, mode: str, merchantId: Optional[str] = None) -> List[dict]:
        """
        Static Method for Parse API Query & Return the Result in List Contains Dictionary

        Args:
            type (str): Specifies the Type of Output Value [count, amount]
            mode (str): Specifies the Type of Report Category [daily, weekly, monthly]
            merchantId (Optional[str]): Mongo ObjectId if not Submit Information of All Users

        Returns:
            A List of Objects Contains key for Horizontal Axis and value for Vertical Axis
        """

        pipeline, case = [], {
            'monthly': '$month',
            'weekly': '$week',
            'daily': '$dayOfYear'
        }
        if merchantId is not None:
            pipeline.append({
                '$match': {'merchantId': ObjectId(merchantId)}
            })
        pipeline.append({
            '$group': {
                '_id': {case[mode]: '$createdAt'},
                'value': {'$sum': 1 if type == 'count' else '$amount'}
            }
        })

        with MongoClient('mongodb://localhost:27017/') as client:
            db = client.zibal
            answer = db.transactions.aggregate(pipeline)

        return [ans for ans in answer]