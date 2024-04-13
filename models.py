from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Определение моделей
class Publisher(Base):
  __tablename__ = 'publisher'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)

  # Обратная связь к книгам
  books = relationship("Book", back_populates="publisher")
class Book(Base):
  __tablename__ = 'book'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

  # Связь с издателем
  publisher = relationship("Publisher", back_populates="books")
  # Связь со stock
  stocks = relationship("Stock", back_populates="book")
class Shop(Base):
  __tablename__ = 'shop'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)

  # Обратная связь к stock
  stocks = relationship("Stock", back_populates="shop")
class Stock(Base):
  __tablename__ = 'stock'

  id = Column(Integer, primary_key=True)
  id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
  id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
  count = Column(Integer, nullable=False)

  # Связь с книгой
  book = relationship("Book", back_populates="stocks")
  # Связь с магазином
  shop = relationship("Shop", back_populates="stocks")
  # Обратная связь к sale
  sales = relationship("Sale", back_populates="stock")
class Sale(Base):
  __tablename__ = 'sale'

  id = Column(Integer, primary_key=True)
  price = Column(Float, nullable=False)
  date_sale = Column(DateTime, default=datetime.utcnow)
  id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
  count = Column(Integer, nullable=False)

  # Связь со stock
  stock = relationship("Stock", back_populates="sales")

# Создание движка SQLAlchemy для PostgreSQL
engine = create_engine('postgresql://postgres:passadmin1@localhost:5432/books', echo=True)

Base.metadata.create_all(engine)

# Создание и использование сессии так же, как было показано ранее