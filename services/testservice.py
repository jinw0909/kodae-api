from fastapi import UploadFile
from sqlalchemy.orm import Session
from io import BytesIO
from datetime import datetime, timedelta
from time import mktime
from random import choice
from db.session import get_db, settings
from db.models import (Test)
from pytz import timezone
import pytz

class MySQLAdapter:
    def __init__(self) -> None:

        # self.KMS_CLIENT= client("kms", region_name='ap-northeast-2')
        self.exchange_id = 1
        self.now = datetime.now(timezone('Asia/Seoul'))
        self.return_dict_data=dict(results=[], reCode=1, message='Server Error')
        self.status_code=200
        self.status=0
        self.check=0
        self.price1=0
    
    
    def get_signal(self,db: Session) :
        
        # Base Declaration

        print('sadsadsadadsa')
        # DB Query
        result = db.query(Test).all()
        for row in result:
            print(row.id)
            print(row.uid)
        