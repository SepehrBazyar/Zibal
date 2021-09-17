from django.db import models
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional, Callable

def cache(function: Callable):
    """
    Decorator for Cache API Query in Another Collection to Faster
    """

    def wrapper(*args, **kwargs):
        res = function(*args, **kwargs)
        with MongoClient('mongodb://localhost:27017/') as client:
            db = client.zibal
            db.cache.insert_one({
                'key': args,
                'value': res
            })
        return res

    return wrapper

# Create your models here.
class Transaction:
    """
    Transaction Class to Management the Query Filter on MongoDB
    """

    @staticmethod
    @cache
    def __result(type: str, mode: str, merchantId: Optional[str] = None) -> List[dict]:
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

    @staticmethod
    def result(type: str, mode: str, merchantId: Optional[str] = None) -> List[dict]:
        """
        Fast Caching Method for Parse API Query & Return the Result in List Contains Dictionary

        Args:
            type (str): Specifies the Type of Output Value [count, amount]
            mode (str): Specifies the Type of Report Category [daily, weekly, monthly]
            merchantId (Optional[str]): Mongo ObjectId if not Submit Information of All Users

        Returns:
            A List of Objects Contains key for Horizontal Axis and value for Vertical Axis
        """

        args = (type, mode, merchantId)
        with MongoClient('mongodb://localhost:27017/') as client:
            db = client.zibal
            res = (db.cache.find_one(
                {
                    'key': args
                },
                {
                    '_id': 0,
                    'key': 0
                }
            ) or {}).get('value', None)
        
        if res is None:
            res = Transaction.__result(*args)
        
        return res
