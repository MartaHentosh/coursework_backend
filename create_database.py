import os
import random
from database import SessionLocal, engine
import models

db_file = "userbase.db"
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Видалено стару базу даних: {db_file}")

# Створюємо всі таблиці заново
models.Base.metadata.create_all(bind=engine)
print("Створено нову базу даних з усіма таблицями")

db = SessionLocal()

try:
    categories_data = [
        {"name": "Піцерії", "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=200&q=80"},
        {"name": "Бургерні", "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200&q=80"},
        {"name": "Кебабні", "image_url": "https://images.unsplash.com/photo-1626082927389-6cd7cdd6cf45?w=200&q=80"},
        {"name": "Суші", "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=200&q=80"},
        {"name": "Азіатська кухня",
         "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200&q=80"},
        {"name": "Сніданки", "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=200&q=80"},
        {"name": "Круасани", "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=200&q=80"},
        {"name": "Кондитерські", "image_url": "https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=200&q=80"},
    ]

    categories = []
    for cat_data in categories_data:
        category = models.Category(**cat_data)
        db.add(category)
        categories.append(category)
        print(f"Додано категорію: {cat_data['name']}")

    db.commit()

    for cat in categories:
        db.refresh(cat)

    category_dict = {cat.name: cat for cat in categories}

    text_filters_data = [
        {"name": "Промокоди"},
        {"name": "Акції"},
        {"name": "На виніс"},
        {"name": "Найпопулярніше"},
    ]

    text_filters = []
    for filter_data in text_filters_data:
        text_filter = models.TextFilter(**filter_data)
        db.add(text_filter)
        text_filters.append(text_filter)
        print(f"Додано текстовий фільтр: {filter_data['name']}")

    db.commit()

    for tf in text_filters:
        db.refresh(tf)

    text_filter_dict = {tf.name: tf for tf in text_filters}

    restaurants_data = [
        {"name": "Піцерія Мілано", "description": "Справжня італійська піца",
         "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&q=80",
         "rating": 4.8, "delivery_time": 30, "delivery_fee": 50.0, "min_order": 200.0, "category": "Піцерії",
         "text_filters": ["Промокоди", "Найпопулярніше"]},
        {"name": "Pizza Express", "description": "Швидка доставка піци",
         "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&q=80",
         "rating": 4.1, "delivery_time": 25, "delivery_fee": 40.0, "min_order": 150.0, "category": "Піцерії",
         "text_filters": ["Акції", "На виніс"]},
        {"name": "Доміно Піца", "description": "Свіжа піца на замовлення",
         "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80",
         "rating": 4.7, "delivery_time": 35, "delivery_fee": 45.0, "min_order": 180.0, "category": "Піцерії",
         "text_filters": ["Найпопулярніше"]},
        {"name": "Піцерія Рома", "description": "Традиційна італійська кухня",
         "image_url": "https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=800&q=80",
         "rating": 4.0, "delivery_time": 40, "delivery_fee": 55.0, "min_order": 220.0, "category": "Піцерії",
         "text_filters": ["Промокоди", "Акції"]},

        {"name": "Burger King", "description": "Класичні бургери та картопля фрі",
         "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80",
         "rating": 4.6, "delivery_time": 25, "delivery_fee": 40.0, "min_order": 150.0, "category": "Бургерні",
         "text_filters": ["Акції", "Найпопулярніше"]},
        {"name": "McDonald's", "description": "Швидка їжа для всієї родини",
         "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&q=80",
         "rating": 4.9, "delivery_time": 20, "delivery_fee": 35.0, "min_order": 120.0, "category": "Бургерні",
         "text_filters": ["Промокоди", "На виніс"]},
        {"name": "Burger House", "description": "Преміум бургери з якісних інгредієнтів",
         "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800&q=80",
         "rating": 4.2, "delivery_time": 30, "delivery_fee": 50.0, "min_order": 200.0, "category": "Бургерні",
         "text_filters": ["Найпопулярніше"]},
        {"name": "Gourmet Burger", "description": "Авторські бургери",
         "image_url": "https://images.unsplash.com/photo-1526234362653-3b75d0a07340?w=800&q=80",
         "rating": 4.1, "delivery_time": 35, "delivery_fee": 60.0, "min_order": 250.0, "category": "Бургерні",
         "text_filters": ["Акції"]},

        {"name": "Кебаб Хаус", "description": "Свіжі кебаби та шаурма",
         "image_url": "https://images.unsplash.com/photo-1626082927389-6cd7cdd6cf45?w=800&q=80",
         "rating": 4.7, "delivery_time": 20, "delivery_fee": 30.0, "min_order": 100.0, "category": "Кебабні",
         "text_filters": ["На виніс", "Найпопулярніше"]},
        {"name": "Шаурма Майстер", "description": "Найкраща шаурма в місті",
         "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800&q=80",
         "rating": 3.9, "delivery_time": 25, "delivery_fee": 35.0, "min_order": 110.0, "category": "Кебабні",
         "text_filters": ["Промокоди"]},
        {"name": "Турецька кухня", "description": "Автентичні турецькі кебаби",
         "image_url": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800&q=80",
         "rating": 4.1, "delivery_time": 30, "delivery_fee": 40.0, "min_order": 130.0, "category": "Кебабні",
         "text_filters": ["Акції", "На виніс"]},

        {"name": "Tokyo Sushi", "description": "Свіжі суші та роли японської кухні",
         "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&q=80",
         "rating": 4.8, "delivery_time": 45, "delivery_fee": 60.0, "min_order": 300.0, "category": "Суші",
         "text_filters": ["Найпопулярніше", "Промокоди"]},
        {"name": "Sushi Master", "description": "Професійні суші від майстрів",
         "image_url": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=800&q=80",
         "rating": 4.7, "delivery_time": 40, "delivery_fee": 55.0, "min_order": 280.0, "category": "Суші",
         "text_filters": ["Акції"]},
        {"name": "Японська кухня", "description": "Традиційні японські страви",
         "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&q=80",
         "rating": 4.1, "delivery_time": 50, "delivery_fee": 65.0, "min_order": 320.0, "category": "Суші",
         "text_filters": ["Найпопулярніше"]},

        {"name": "Wok Express", "description": "Швидка азійська кухня на винесення",
         "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80",
         "rating": 4.4, "delivery_time": 25, "delivery_fee": 35.0, "min_order": 120.0, "category": "Азіатська кухня",
         "text_filters": ["На виніс", "Акції"]},
        {"name": "Китайська кухня", "description": "Автентичні китайські страви",
         "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80",
         "rating": 4.5, "delivery_time": 30, "delivery_fee": 40.0, "min_order": 150.0, "category": "Азіатська кухня",
         "text_filters": ["Промокоди"]},
        {"name": "Тайська кухня", "description": "Пікантні тайські страви",
         "image_url": "https://images.unsplash.com/photo-1559314809-0c8cc0b8b0b8?w=800&q=80",
         "rating": 3.8, "delivery_time": 35, "delivery_fee": 45.0, "min_order": 180.0, "category": "Азіатська кухня",
         "text_filters": ["Найпопулярніше", "Акції"]},
        {"name": "В'єтнамська кухня", "description": "Свіжі в'єтнамські страви",
         "image_url": "https://images.unsplash.com/photo-1546069901-ec6473dfe7b1?w=800&q=80",
         "rating": 4.1, "delivery_time": 30, "delivery_fee": 40.0, "min_order": 160.0, "category": "Азіатська кухня",
         "text_filters": ["На виніс"]},

        {"name": "Сніданок & Кава", "description": "Смачні сніданки та гаряча кава",
         "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800&q=80",
         "rating": 4.6, "delivery_time": 20, "delivery_fee": 30.0, "min_order": 100.0, "category": "Сніданки",
         "text_filters": ["Промокоди", "На виніс"]},
        {"name": "Ранкова кава", "description": "Свіжі сніданки з ранку",
         "image_url": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800&q=80",
         "rating": 4.0, "delivery_time": 25, "delivery_fee": 35.0, "min_order": 110.0, "category": "Сніданки",
         "text_filters": ["Акції"]},
        {"name": "Brunch Cafe", "description": "Розкішні бранчі та сніданки",
         "image_url": "https://images.unsplash.com/photo-1506084868230-bb9d95c24759?w=800&q=80",
         "rating": 4.7, "delivery_time": 30, "delivery_fee": 40.0, "min_order": 150.0, "category": "Сніданки",
         "text_filters": ["Найпопулярніше"]},

        {"name": "Круасани Париж", "description": "Французькі круасани та випічка",
         "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800&q=80",
         "rating": 4.3, "delivery_time": 20, "delivery_fee": 25.0, "min_order": 80.0, "category": "Круасани",
         "text_filters": ["Промокоди", "На виніс"]},
        {"name": "Boulangerie", "description": "Свіжа французька випічка",
         "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&q=80",
         "rating": 3.7, "delivery_time": 25, "delivery_fee": 30.0, "min_order": 90.0, "category": "Круасани",
         "text_filters": ["Акції"]},
        {"name": "Круасани & Кава", "description": "Свіжі круасани та ароматна кава",
         "image_url": "https://images.unsplash.com/photo-1519869325934-281144150011?w=800&q=80",
         "rating": 4.6, "delivery_time": 22, "delivery_fee": 28.0, "min_order": 85.0, "category": "Круасани",
         "text_filters": ["Найпопулярніше"]},

        {"name": "Sweet Dreams", "description": "Домашні десерти та торти",
         "image_url": "https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800&q=80",
         "rating": 4.8, "delivery_time": 35, "delivery_fee": 45.0, "min_order": 180.0, "category": "Кондитерські",
         "text_filters": ["Промокоди", "Акції"]},
        {"name": "Кондитерська Майстерня", "description": "Авторські торти та десерти",
         "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80",
         "rating": 4.0, "delivery_time": 40, "delivery_fee": 50.0, "min_order": 200.0, "category": "Кондитерські",
         "text_filters": ["Найпопулярніше"]},
        {"name": "Цукерня", "description": "Традиційні солодощі та цукерки",
         "image_url": "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6d?w=800&q=80",
         "rating": 4.5, "delivery_time": 30, "delivery_fee": 40.0, "min_order": 150.0, "category": "Кондитерські",
         "text_filters": ["На виніс"]},
        {"name": "Шоколадна фабрика", "description": "Шоколадні десерти та цукерки",
         "image_url": "https://images.unsplash.com/photo-1606312619070-d48b4e6b3c5e?w=800&q=80",
         "rating": 4.2, "delivery_time": 35, "delivery_fee": 45.0, "min_order": 170.0, "category": "Кондитерські",
         "text_filters": ["Промокоди", "Найпопулярніше"]},
        {"name": "Тортова майстерня", "description": "Святкові торти на замовлення",
         "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80",
         "rating": 3.9, "delivery_time": 45, "delivery_fee": 55.0, "min_order": 250.0, "category": "Кондитерські",
         "text_filters": ["Акції", "На виніс"]},
    ]

    random.seed(42)

    for rest_data in restaurants_data:
        category_name = rest_data.pop("category")
        text_filter_names = rest_data.pop("text_filters", [])

        category = category_dict[category_name]

        distance = round(random.uniform(1.2, 20.0), 1)

        restaurant = models.Restaurant(
            name=rest_data["name"],
            description=rest_data["description"],
            image_url=rest_data["image_url"],
            rating=rest_data["rating"],
            delivery_time=rest_data["delivery_time"],
            delivery_fee=rest_data["delivery_fee"],
            min_order=rest_data["min_order"],
            distance=distance,
            is_active=1
        )

        restaurant.categories.append(category)

        for tf_name in text_filter_names:
            if tf_name in text_filter_dict:
                restaurant.text_filters.append(text_filter_dict[tf_name])

        db.add(restaurant)
        print(
            f"Додано ресторан: {rest_data['name']} (відстань: {distance} км, категорія: {category_name}, фільтри: {', '.join(text_filter_names)})")

    db.commit()

    print(f"\nГотово! Створено базу даних з:")
    print(f"   - {len(categories)} категоріями")
    print(f"   - {len(text_filters)} текстовими фільтрами")
    print(f"   - {len(restaurants_data)} ресторанами")
    print(f"   - Всі ресторани мають випадкову відстань від 1.2 до 20 км")
    print(f"   - Всі ресторани зв'язані з категоріями та текстовими фільтрами")

except Exception as e:
    db.rollback()
    print(f"Помилка при створенні бази даних: {e}")
    raise
finally:
    db.close()
