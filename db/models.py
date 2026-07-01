from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, Text, Float, DOUBLE, BLOB, DATETIME
from db.session import Base



# DB Class
class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    retri_id = Column(VARCHAR(32), nullable=True)
    uid = Column(VARCHAR(128, collation="utf8mb4_0900_ai_ci"), nullable=True)
    exchange = Column(Integer, nullable=True)
    datetime = Column(DATETIME, nullable=True)
    main_id = Column(VARCHAR(100), nullable=True)
    admin = Column(VARCHAR(100), nullable=True)
    
# DB Class
class WebhookLog(Base):
    __tablename__ = 'webhook_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(VARCHAR(100), nullable=True)
    payment_key = Column(VARCHAR(100), nullable=True)
    status = Column(VARCHAR(100), nullable=True)
    payload=Column(Text, nullable=True)
    datetime=Column(DATETIME, nullable=False)
    
    
class WebhookLogHistory(Base):
    __tablename__ = "webhook_log_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(VARCHAR(100))
    payment_key = Column(VARCHAR(200))
    status = Column(VARCHAR(50))
    payload = Column(Text)
    datetime = Column(DATETIME(timezone=True))
    
    
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(VARCHAR(255), unique=True, nullable=False, index=True)

    user_id = Column(Integer, nullable=True)

    product_name = Column(VARCHAR(255), nullable=True)

    amount = Column(Integer, nullable=True)

    status = Column(VARCHAR(50), nullable=True, default="WAITING_PAYMENT")

    datetime = Column(DATETIME, nullable=True)