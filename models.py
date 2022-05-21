from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    balance = Column(Integer, nullable=False)
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, barcode={self.barcode!r}, balance={self.balance!r}"

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    barcode = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    type = Column(String(30), nullable=False)
    amount = Column(Integer, nullable=False)
    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.name!r}, barcode={self.barcode!r}, price={self.price!r}, amount={self.amount!r}"

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    state = Column(String(30), nullable=False)
    deposited = Column(Integer, nullable=False)
    def __repr__(self):
        return f"Log(id={self.id!r}, time_created={self.time_created!r}, user_id={self.user_id!r}, state={self.state!r}, deposited={self.deposited!r}"

class LogProduct(Base):
    __tablename__ = "logproduct"
    id = Column(Integer, primary_key=True)
    log_id = Column(Integer, ForeignKey("log.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    def __repr__(self):
        return f"LogProduct(id={self.id!r}, log_id={self.log_id!r}, product_id={self.product_id!r}"

class Font(Base):
    __tablename__ = "font"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    score = Column(Integer, nullable=False)
    def __repr__(self):
        return f"Font(id={self.id!r}, name={self.name!r}, score={self.score!r}"
