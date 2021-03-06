from django.db import models
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional, Callable
from datetime import datetime, timedelta
from calendar import month_name

def normalize(pk: int, year: int, mode: str) -> str:
    """
    Generate Standard Output for API by Get the Mode & Primary Key Result
    """

    if mode == 'monthly':
        return f"{month_name[pk]} {year}"
    elif mode == 'weekly':
        return f"Week {pk} Year {year}"
    else:
        date = datetime(year, 1, 1) + timedelta(pk - 1)

    return f"{year}/{date.month}/{date.day}"

def cache(function: Callable):
    """
    Decorator for Cache API Query in Another Collection to Faster
    """

    def wrapper(*args, **kwargs):
        res = function(*args, **kwargs)

        with MongoClient('mongodb://localhost:27017/') as client:
            db = client.zibal

            if db.cache.count_documents({}) == 0:
                db.cache.create_index('key')

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

        pipeline.extend([{
            '$group': {
                '_id': {
                    'pk': {
                        case[mode]: '$createdAt'
                    },
                    'year': {
                        '$year': '$createdAt'
                    }
                },
                'value': {
                    '$sum': 1 if type == 'count' else '$amount'
                }
            }
        },{
            '$sort': {
                '_id.year': 1,
                '_id.pk': 1
            }
        }])

        with MongoClient('mongodb://localhost:27017/') as client:
            db = client.zibal
            answer = db.transactions.aggregate(pipeline)

        return [{
            'key': normalize(ans['_id']['pk'], ans['_id']['year'], mode),
            'value': ans['value']
        } for ans in answer]

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
            res = db.cache.find_one(
                {
                    'key': args
                },
                {
                    '_id': 0,
                    'key': 0
                }
            ) or {}
        
        return res.get('value') if 'value' in res else Transaction.__result(*args)
