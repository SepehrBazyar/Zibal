from django.core.management.base import BaseCommand, CommandError
from pymongo import MongoClient
from argparse import ArgumentParser
from typing import Any, Optional
from bson import decode_all

class Command(BaseCommand):
    """
    Command Class to Migrate BSON Data to MongoDB
    """

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('path', metavar='PATH', help="Please Enter File Name.")
    
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        path = options['path']
        try:
            with open(path, mode='rb') as fl:
                data = decode_all(fl.read())
        except FileNotFoundError:
            raise CommandError(f"{path} File Does Not Exist in This Directory.")
        else:
            with MongoClient('mongodb://localhost:27017/') as client:
                db = client.zibal
                db.transactions.insert_many(data)
            self.stdout.write(self.style.SUCCESS(f"{path} File Migrated to the MongoDB."))
