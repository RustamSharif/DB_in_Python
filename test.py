import json
import os
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from models import Publisher, Shop, Book, Stock, Sale, engine

# Загрузка настроек из переменных окружения
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'passadmin1')
db_host = os.getenv('DB_HOST', 'localhost')
db_name = os.getenv('DB_NAME', 'books')
db_port = os.getenv('DB_PORT', '5432')
dsn = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Обновление движка с учетом загруженных настроек
engine = create_engine(dsn, echo=True)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r', encoding='utf-8') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()

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