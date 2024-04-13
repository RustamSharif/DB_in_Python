# Предполагается, что вы уже импортировали модели и создали движок SQLAlchemy.
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from models import engine

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Получаем имя или идентификатор издателя от пользователя
publisher_input = input("Введите имя или идентификатор издателя: ")

try:
    # Преобразуем ввод в integer, если это возможно, в противном случае ищем по имени
    publisher_id = int(publisher_input)
    condition = Publisher.id == publisher_id
except ValueError:
    condition = Publisher.name == publisher_input

# Формируем запрос
results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
    .join(Publisher)\
    .join(Stock, Book.id == Stock.id_book)\
    .join(Shop, Stock.id_shop == Shop.id)\
    .join(Sale, Stock.id == Sale.id_stock)\
    .filter(condition).all()

# Вывод результатов
for title, shop_name, price, date_sale in results:
    print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")

# Закрываем сессию
session.close()