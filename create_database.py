import os
import random
from database import SessionLocal, engine
import models
from passlib.context import CryptContext

db_file = "userbase.db"
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Видалено стару базу даних: {db_file}")

# Створюємо всі таблиці заново
models.Base.metadata.create_all(bind=engine)
print("Створено нову базу даних з усіма таблицями")

db = SessionLocal()

crypt = CryptContext(schemes=['bcrypt'], deprecated='auto')

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
        {"name": "Піцерія Мілано", "description": "Справжня італійська піца", "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&q=80",
         "rating": 4.8, "delivery_time": 30, "delivery_fee": 50.0, "min_order": 200.0, "category": "Піцерії", "text_filters": ["Промокоди", "Найпопулярніше"]},
        {"name": "Pizza Express", "description": "Швидка доставка піци", "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&q=80", 
         "rating": 4.1, "delivery_time": 25, "delivery_fee": 40.0, "min_order": 150.0, "category": "Піцерії", "text_filters": ["Акції", "На виніс"]},
        {"name": "Доміно Піца", "description": "Свіжа піца на замовлення", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80", 
         "rating": 4.7, "delivery_time": 35, "delivery_fee": 45.0, "min_order": 180.0, "category": "Піцерії", "text_filters": ["Найпопулярніше"]},
        {"name": "Піцерія Рома", "description": "Традиційна італійська кухня", "image_url": "https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=800&q=80", 
         "rating": 4.0, "delivery_time": 40, "delivery_fee": 55.0, "min_order": 220.0, "category": "Піцерії", "text_filters": ["Промокоди", "Акції"]},
        
        {"name": "Burger King", "description": "Класичні бургери та картопля фрі", "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80",
         "rating": 4.6, "delivery_time": 25, "delivery_fee": 40.0, "min_order": 150.0, "category": "Бургерні", "text_filters": ["Акції", "Найпопулярніше"]},
        {"name": "McDonald's", "description": "Швидка їжа для всієї родини", "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&q=80", 
         "rating": 4.9, "delivery_time": 20, "delivery_fee": 35.0, "min_order": 120.0, "category": "Бургерні", "text_filters": ["Промокоди", "На виніс"]},
        {"name": "Burger House", "description": "Преміум бургери з якісних інгредієнтів", "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800&q=80", 
         "rating": 4.2, "delivery_time": 30, "delivery_fee": 50.0, "min_order": 200.0, "category": "Бургерні", "text_filters": ["Найпопулярніше"]},
        {"name": "Gourmet Burger", "description": "Авторські бургери", "image_url": "https://images.unsplash.com/photo-1526234362653-3b75d0a07340?w=800&q=80", 
         "rating": 4.1, "delivery_time": 35, "delivery_fee": 60.0, "min_order": 250.0, "category": "Бургерні", "text_filters": ["Акції"]},
        
        {"name": "Кебаб Хаус", "description": "Свіжі кебаби та шаурма", "image_url": "https://images.unsplash.com/photo-1626082927389-6cd7cdd6cf45?w=800&q=80",
         "rating": 4.7, "delivery_time": 20, "delivery_fee": 30.0, "min_order": 100.0, "category": "Кебабні", "text_filters": ["На виніс", "Найпопулярніше"]},
        {"name": "Шаурма Майстер", "description": "Найкраща шаурма в місті", "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800&q=80", 
         "rating": 3.9, "delivery_time": 25, "delivery_fee": 35.0, "min_order": 110.0, "category": "Кебабні", "text_filters": ["Промокоди"]},
        {"name": "Турецька кухня", "description": "Автентичні турецькі кебаби", "image_url": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800&q=80", 
         "rating": 4.1, "delivery_time": 30, "delivery_fee": 40.0, "min_order": 130.0, "category": "Кебабні", "text_filters": ["Акції", "На виніс"]},
        
        {"name": "Tokyo Sushi", "description": "Свіжі суші та роли японської кухні", "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&q=80",
         "rating": 4.8, "delivery_time": 45, "delivery_fee": 60.0, "min_order": 300.0, "category": "Суші", "text_filters": ["Найпопулярніше", "Промокоди"]},
        {"name": "Sushi Master", "description": "Професійні суші від майстрів", "image_url": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=800&q=80", 
         "rating": 4.7, "delivery_time": 40, "delivery_fee": 55.0, "min_order": 280.0, "category": "Суші", "text_filters": ["Акції"]},
        {"name": "Японська кухня", "description": "Традиційні японські страви", "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&q=80", 
         "rating": 4.1, "delivery_time": 50, "delivery_fee": 65.0, "min_order": 320.0, "category": "Суші", "text_filters": ["Найпопулярніше"]},
        
        {"name": "Wok Express", "description": "Швидка азійська кухня на винесення", "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80",
         "rating": 4.4, "delivery_time": 25, "delivery_fee": 35.0, "min_order": 120.0, "category": "Азіатська кухня", "text_filters": ["На виніс", "Акції"]},
        {"name": "Китайська кухня", "description": "Автентичні китайські страви", "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80", 
         "rating": 4.5, "delivery_time": 30, "delivery_fee": 40.0, "min_order": 150.0, "category": "Азіатська кухня", "text_filters": ["Промокоди"]},
        
        {"name": "Сніданок & Кава", "description": "Смачні сніданки та гаряча кава", "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=800&q=80",
         "rating": 4.6, "delivery_time": 20, "delivery_fee": 30.0, "min_order": 100.0, "category": "Сніданки", "text_filters": ["Промокоди", "На виніс"]},
        {"name": "Ранкова кава", "description": "Свіжі сніданки з ранку", "image_url": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800&q=80", 
         "rating": 4.0, "delivery_time": 25, "delivery_fee": 35.0, "min_order": 110.0, "category": "Сніданки", "text_filters": ["Акції"]},
        
        {"name": "Круасани Париж", "description": "Французькі круасани та випічка", "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800&q=80",
         "rating": 4.3, "delivery_time": 20, "delivery_fee": 25.0, "min_order": 80.0, "category": "Круасани", "text_filters": ["Промокоди", "На виніс"]},
        {"name": "Boulangerie", "description": "Свіжа французька випічка", "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&q=80", 
         "rating": 3.7, "delivery_time": 25, "delivery_fee": 30.0, "min_order": 90.0, "category": "Круасани", "text_filters": ["Акції"]},
        
        {"name": "Sweet Dreams", "description": "Домашні десерти та торти", "image_url": "https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800&q=80",
         "rating": 4.8, "delivery_time": 35, "delivery_fee": 45.0, "min_order": 180.0, "category": "Кондитерські", "text_filters": ["Промокоди", "Акції"]},
        {"name": "Кондитерська Майстерня", "description": "Авторські торти та десерти", "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80", 
         "rating": 4.0, "delivery_time": 40, "delivery_fee": 50.0, "min_order": 200.0, "category": "Кондитерські", "text_filters": ["Найпопулярніше"]},
    ]

    dishes_data = [

        {'name': 'Маргарита', 'description': 'Класична італійська піца з моцарелою', 'price': 110.0, 'weight': 430, 'image_url': 'https://lviv.veteranopizza.com/image/catalog/pizza/margo.jpg', 'restaurant_idx': 0},
        {'name': 'Пепероні', 'description': 'Піца з пряною салямі', 'price': 120.0, 'weight': 420, 'image_url': 'https://lviv.veteranopizza.com/image/catalog/pizza/peperoni.jpg', 'restaurant_idx': 0},
        {'name': '4 сири', 'description': 'Піца із сумішшю сирів', 'price': 128.0, 'weight': 445, 'image_url': 'https://street-food.com.ua/wp-content/uploads/2022/10/chetyre-syra.png', 'restaurant_idx': 0},
        {'name': 'Гавайська', 'description': 'Піца з ананасом і шинкою', 'price': 124.0, 'weight': 430, 'image_url': 'https://lviv.veteranopizza.com/image/catalog/pizza/gavajska.jpg', 'restaurant_idx': 0},
        {'name': 'Мексиканська', 'description': 'Гостра піца із ковбасками', 'price': 129.0, 'weight': 440, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBrdsWoJGraaDEx4lXXB1j8Dn2PdCmJ219gA&s', 'restaurant_idx': 0},
        {'name': 'Вегетаріанська', 'description': 'Піца для вегетаріанців', 'price': 112.0, 'weight': 425, 'image_url': 'https://assets.dots.live/misteram-public/0195d7c3-976c-7388-b167-65012c60fe07-826x0.png', 'restaurant_idx': 0},

        {'name': 'Карбонара', 'description': 'Піца з беконом і вершковим соусом', 'price': 134.0, 'weight': 460, 'image_url': 'https://media-v3.dominos.ua/Products/karbonara-300dpi.webp', 'restaurant_idx': 1},
        {'name': 'Барбекю', 'description': 'Піца із соусом барбекю', 'price': 130.0, 'weight': 435, 'image_url': 'https://media-v3.dominos.ua/Products/bbq-delux-300dpi-min.webp', 'restaurant_idx': 1},
        {'name': 'Морська', 'description': 'Піца з морепродуктами', 'price': 145.0, 'weight': 420, 'image_url': 'https://media-v3.dominos.ua/Products/Pitsa/Pitsy/beefandCrispy/new/beefandcrispy-pieces.webp', 'restaurant_idx': 1},
        {'name': 'Аміго', 'description': 'Піца з соусами і двома видами сирів', 'price': 122.0, 'weight': 410, 'image_url': 'https://media-v3.dominos.ua/Products/extravaganzza-slice1-min.webp', 'restaurant_idx': 1},
        {'name': 'Капрічоза', 'description': 'Піца з ковбасою і грибами', 'price': 138.0, 'weight': 425, 'image_url': 'https://media-v3.dominos.ua/Products/Pitsa/Pitsy/Sweet/06_06/pizza-sweet-website-main.webp', 'restaurant_idx': 1},
        {'name': 'Неаполітанська', 'description': 'Традиційна піца із томатами, оливками', 'price': 117.0, 'weight': 418, 'image_url': 'https://media-v3.dominos.ua/Products/grill-slice-collageweb-min.webp', 'restaurant_idx': 1},

        {'name': 'Доміно Класік', 'description': 'Домашня піца з беконом та сиром', 'price': 135.0, 'weight': 440, 'image_url': 'https://i.pinimg.com/1200x/e0/c5/b5/e0c5b5ee8e4c56894a8550da6c789d73.jpg', 'restaurant_idx': 2},
        {'name': 'Піца Торіно', 'description': 'З в’яленими томатами та оливками', 'price': 130.0, 'weight': 420, 'image_url': 'https://i.pinimg.com/1200x/f8/88/72/f888722ed3ce49d0dab0c9e3c8d14491.jpg', 'restaurant_idx': 2},
        {'name': 'Міланська', 'description': 'Копчена шинка та гриби', 'price': 128.0, 'weight': 435, 'image_url': 'https://i.pinimg.com/736x/61/29/9d/61299d2d40511d3fe8649f32f0b5146f.jpg', 'restaurant_idx': 2},
        {'name': 'Сир і шинка', 'description': 'Сирний мікс, шинка, вершковий соус', 'price': 120.0, 'weight': 425, 'image_url': 'https://i.pinimg.com/1200x/93/44/3e/93443e7d168dbdfe01244fc2f25cc1f4.jpg', 'restaurant_idx': 2},
        {'name': 'Піца з куркою', 'description': 'Курячі шматочки, зелень, моцарела', 'price': 138.0, 'weight': 440, 'image_url': 'https://i.pinimg.com/736x/e5/80/f5/e580f58da7814e103eb859ed80d684eb.jpg', 'restaurant_idx': 2},
        {'name': 'Фірмова Доміно', 'description': 'Італійські ковбаски, перець, цибуля', 'price': 140.0, 'weight': 450, 'image_url': 'https://i.pinimg.com/1200x/ad/60/0e/ad600e9023ff5184236b3dd1e6ef8bbb.jpg', 'restaurant_idx': 2},

        {'name': 'Рома Особлива', 'description': 'Вітчина, моцарела, зелень', 'price': 125.0, 'weight': 420, 'image_url': 'https://i.pinimg.com/736x/8d/40/f0/8d40f08f17068593395bdad90eccc67d.jpg', 'restaurant_idx': 3},
        {'name': 'Чотири сезони', 'description': 'Копченості, овочі, іт. сир', 'price': 132.0, 'weight': 435, 'image_url': 'https://i.pinimg.com/1200x/46/7e/cf/467ecf2544d1dabfa7e1ff5254d91b96.jpg', 'restaurant_idx': 3},
        {'name': 'Грибна', 'description': 'Сир, мариновані гриби, сметанний соус', 'price': 128.0, 'weight': 415, 'image_url': 'https://i.pinimg.com/736x/f6/d3/e5/f6d3e5d90e484c5c62da7aecec198c79.jpg', 'restaurant_idx': 3},
        {'name': 'Прошуто', 'description': 'Прошуто, помідори, моцарела', 'price': 139.0, 'weight': 440, 'image_url': 'https://i.pinimg.com/1200x/21/79/2e/21792eafb3bd4d97adca552ea4c13739.jpg', 'restaurant_idx': 3},
        {'name': 'Піца Барбекю', 'description': 'Курка, соус барбекю, перець', 'price': 134.0, 'weight': 435, 'image_url': 'https://i.pinimg.com/1200x/6b/aa/63/6baa6388ecf7742f0937c12ea6abea11.jpg', 'restaurant_idx': 3},
        {'name': 'Піца з маслинами', 'description': 'Сир, маслини, базилік', 'price': 120.0, 'weight': 400, 'image_url': 'https://i.pinimg.com/1200x/1e/cf/97/1ecf97063960bbfb8456125e4c323381.jpg', 'restaurant_idx': 3},

        {'name': 'Воппер', 'description': 'Яловичина, сир, овочі, соус', 'price': 92.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/1200x/65/b7/8b/65b78bf00f5a87e5105d2b1cc0759d5f.jpg', 'restaurant_idx': 4},
        {'name': 'Чікен-Бургер', 'description': 'Котлета з курки, салат, соус', 'price': 77.0, 'weight': 210, 'image_url': 'https://i.pinimg.com/1200x/f0/83/12/f08312b5b45b888622e24921df51cb4d.jpg', 'restaurant_idx': 4},
        {'name': 'Кінг Фіш', 'description': 'Риба, хрустка булка, салат айсберг', 'price': 86.0, 'weight': 175, 'image_url': 'https://i.pinimg.com/736x/85/9d/2d/859d2dc17a7bee87590ec145e4263eae.jpg', 'restaurant_idx': 4},
        {'name': 'Картошка-Фрі', 'description': 'Класична по-бургеркінгівськи', 'price': 48.0, 'weight': 120, 'image_url': 'https://i.pinimg.com/736x/72/b5/a1/72b5a16458ea71865ecc8189a3bf42eb.jpg', 'restaurant_idx': 4},
        {'name': 'Сирні палички', 'description': 'Тягучий сир у клярі', 'price': 51.0, 'weight': 100, 'image_url': 'https://i.pinimg.com/1200x/43/e5/45/43e545d16cd881f4c2d6bd3bd1275df6.jpg', 'restaurant_idx': 4},
        {'name': 'Кінг-Бургер XXL', 'description': 'Подвійна котлета, подвійний сир', 'price': 115.0, 'weight': 330, 'image_url': 'https://i.pinimg.com/1200x/b9/05/0a/b9050a9ef4a6799b067effcde63ff4fb.jpg', 'restaurant_idx': 4},

        {'name': 'Біг Мак', 'description': 'Яловичина, булка з кунжутом, спеції', 'price': 99.0, 'weight': 225, 'image_url': 'https://i.pinimg.com/736x/e0/41/55/e04155f66d448ef2c5c8a1e6bf0e546e.jpg', 'restaurant_idx': 5},
        {'name': 'Чікен Макнагетс', 'description': 'Курячі нагетси, соуси', 'price': 75.0, 'weight': 110, 'image_url': 'https://i.pinimg.com/736x/bb/13/40/bb1340e0679ddf9ac560b26c435a669b.jpg ', 'restaurant_idx': 5},
        {'name': 'Філе-О-Фіш', 'description': 'Рибна котлета, сир, булка', 'price': 87.0, 'weight': 160, 'image_url': 'https://i.pinimg.com/1200x/1b/22/0f/1b220f8e09a3afaf37fc6aaad4cfff3a.jpg', 'restaurant_idx': 5},
        {'name': 'Картопля по-селянськи', 'description': 'Запечена картопля', 'price': 49.0, 'weight': 130, 'image_url': 'https://i.pinimg.com/1200x/fd/9b/2e/fd9b2e5235c42983e5983a0018533d6f.jpg', 'restaurant_idx': 5},
        {'name': 'МакЧікен', 'description': 'Котлета, салат, майонез', 'price': 79.0, 'weight': 180, 'image_url': 'https://i.pinimg.com/1200x/ee/bd/4c/eebd4c81da8b662aafdaef3a45b0711b.jpg', 'restaurant_idx': 5},
        {'name': 'МакФлурі', 'description': 'Десерт з морозивом і топінгом', 'price': 55.0, 'weight': 150, 'image_url': 'https://i.pinimg.com/736x/29/ac/24/29ac243ac20674b53a0b4679c078e2a5.jpg', 'restaurant_idx': 5},

        {'name': 'Домашній бургер', 'description': 'Яловичина, подвійний сир, помідор', 'price': 108.0, 'weight': 290, 'image_url': 'https://i.pinimg.com/736x/a0/91/10/a09110eb81d7611e12b93e9e610cd2a7.jpg', 'restaurant_idx': 6},
        {'name': 'Чізбургер преміум', 'description': 'Витриманий чеддер, бекон', 'price': 113.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/736x/f2/18/49/f21849411b88b1901af9bb3f25f2c57c.jpg', 'restaurant_idx': 6},
        {'name': 'Класичний курячий', 'description': 'Курка гриль, салат, соус', 'price': 96.0, 'weight': 240, 'image_url': 'https://i.pinimg.com/736x/2c/ed/cf/2cedcf49a0d64dc927f48787e2918fcb.jpg', 'restaurant_idx': 6},
        {'name': 'Пепер-гриль', 'description': 'Яловичина, гірчичний соус, зелень', 'price': 115.0, 'weight': 270, 'image_url': 'https://i.pinimg.com/1200x/8a/91/9d/8a919d393020ac58df20094e089e9dcc.jpg', 'restaurant_idx': 6},
        {'name': 'Фірмовий бургер', 'description': 'Фірмовий соус, овочі, котлета', 'price': 119.0, 'weight': 310, 'image_url': 'https://i.pinimg.com/1200x/14/61/4e/14614eb7538b0b8e448950356ac40b03.jpg', 'restaurant_idx': 6},
        {'name': 'Овочевий бургер', 'description': 'Свіжі овочі, сир, булка з кунжутом', 'price': 99.0, 'weight': 210, 'image_url': 'https://i.pinimg.com/1200x/f6/b5/e9/f6b5e91a53ba29e1ece79f6467636042.jpg', 'restaurant_idx': 6},

        {'name': 'Гурман бургер', 'description': 'Авторський бургер з витриманим сиром', 'price': 125.0, 'weight': 320, 'image_url': 'https://i.pinimg.com/1200x/68/3c/0a/683c0ac1946881e4515f2a6f8d3774eb.jpg', 'restaurant_idx': 7},
        {'name': 'Трюфельний бургер', 'description': 'Преміум бургер з трюфельним соусом', 'price': 145.0, 'weight': 340, 'image_url': 'https://i.pinimg.com/1200x/1e/e1/45/1ee1458739390f175b646b2788e8e48e.jpg', 'restaurant_idx': 7},
        {'name': 'Бургер з яловичиною вагю', 'description': 'Преміум м\'ясо вагю, сир, овочі', 'price': 165.0, 'weight': 350, 'image_url': 'https://i.pinimg.com/1200x/27/9b/9f/279b9f1f7e54856565ec8f3c76062adc.jpg', 'restaurant_idx': 7},
        {'name': 'Бургер з беконом', 'description': 'Хрусткий бекон, сир чеддер, соус', 'price': 118.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/736x/c9/c5/01/c9c5013a47c78dde12d22a8659cdb945.jpg', 'restaurant_idx': 7},
        {'name': 'Вегетаріанський гурман', 'description': 'Авторський вегетаріанський бургер', 'price': 105.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/736x/63/25/0d/63250d14bc1a1f43a7e158bfe05574f2.jpg', 'restaurant_idx': 7},
        {'name': 'Бургер з сиром дор блю', 'description': 'Преміум сир дор блю, яловичина', 'price': 135.0, 'weight': 310, 'image_url': 'https://i.pinimg.com/736x/8a/7b/78/8a7b78f884dbedb703c7002bd0a9388d.jpg', 'restaurant_idx': 7},

        {'name': 'Класичний кебаб', 'description': 'Свіже м\'ясо, овочі, соус', 'price': 85.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/1200x/b8/cf/af/b8cfaf3c8fa3cdf8373933fece2ee71f.jpg', 'restaurant_idx': 8},
        {'name': 'Кебаб з куркою', 'description': 'Куряче м\'ясо, свіжі овочі', 'price': 78.0, 'weight': 260, 'image_url': 'https://i.pinimg.com/736x/ab/10/fd/ab10fdb1ca61f920f60084fbe25f223d.jpg', 'restaurant_idx': 8},
        {'name': 'Кебаб мікс', 'description': 'Суміш м\'яса, овочі, соуси', 'price': 92.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/736x/3d/e7/66/3de7660996a24057fb50f57b3e0b1f16.jpg', 'restaurant_idx': 8},
        {'name': 'Кебаб з яловичиною', 'description': 'Ніжна яловичина, овочі', 'price': 88.0, 'weight': 270, 'image_url': 'https://i.pinimg.com/1200x/12/04/90/1204904925e126e2b3de2e933762735a.jpg', 'restaurant_idx': 8},
        {'name': 'Кебаб з бараниною', 'description': 'Автентична баранина, спеції', 'price': 95.0, 'weight': 290, 'image_url': 'https://i.pinimg.com/736x/f2/bc/33/f2bc33e2b66c0a7e3f8fe1165d307d89.jpg', 'restaurant_idx': 8},
        {'name': 'Кебаб вегетаріанський', 'description': 'Овочі гриль, соуси', 'price': 72.0, 'weight': 240, 'image_url': 'https://i.pinimg.com/1200x/2e/f9/dd/2ef9dd6cea91af8a230537e03c1a3f60.jpg', 'restaurant_idx': 8},

        {'name': 'Шаурма класична', 'description': 'Свіже м\'ясо, овочі, соус', 'price': 75.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/736x/b2/38/d8/b238d8b6bb0485656b9454db7b3634a5.jpg', 'restaurant_idx': 9},
        {'name': 'Шаурма з куркою', 'description': 'Куряче м\'ясо, свіжі овочі', 'price': 70.0, 'weight': 230, 'image_url': 'https://i.pinimg.com/736x/13/90/32/13903285638a317e43b79bba17579114.jpg    ', 'restaurant_idx': 9},
        {'name': 'Шаурма з яловичиною', 'description': 'Ніжна яловичина, овочі', 'price': 80.0, 'weight': 260, 'image_url': 'https://i.pinimg.com/736x/39/9b/66/399b669664b13e4f832e3ef4f39ea259.jpg', 'restaurant_idx': 9},
        {'name': 'Шаурма мікс', 'description': 'Суміш м\'яса, овочі, соуси', 'price': 85.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/1200x/cc/dc/6a/ccdc6a73a516460c9ad89d95830cccd2.jpg', 'restaurant_idx': 9},
        {'name': 'Шаурма з бараниною', 'description': 'Автентична баранина, спеції', 'price': 88.0, 'weight': 270, 'image_url': 'https://i.pinimg.com/736x/04/8d/5c/048d5c7ab2716039d623d8c9ae5e1f3a.jpg', 'restaurant_idx': 9},
        {'name': 'Шаурма вегетаріанська', 'description': 'Овочі гриль, соуси', 'price': 65.0, 'weight': 220, 'image_url': 'https://i.pinimg.com/736x/ab/9f/97/ab9f9710642147c95dbb24c58f85c5e1.jpg', 'restaurant_idx': 9},

        {'name': 'Турецький кебаб', 'description': 'Автентичний турецький кебаб', 'price': 90.0, 'weight': 290, 'image_url': 'https://i.pinimg.com/1200x/2b/5b/ed/2b5bed0f8e21e5e5638a0ec062872b8d.jpg', 'restaurant_idx': 10},
        {'name': 'Донер кебаб', 'description': 'Традиційний донер з яловичиною', 'price': 88.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/1200x/18/0b/81/180b811e3ab160e76896e86ce0171aa5.jpg', 'restaurant_idx': 10},
        {'name': 'Іскендер кебаб', 'description': 'Класичний іскендер з йогуртом', 'price': 95.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/1200x/bc/a6/7b/bca67bb541c6aa746c365a61f1158c0e.jpg', 'restaurant_idx': 10},
        {'name': 'Адана кебаб', 'description': 'Гострий кебаб з баранини', 'price': 92.0, 'weight': 285, 'image_url': 'https://i.pinimg.com/1200x/2c/c8/df/2cc8dfab5e2fd5e908b64deca8078df1.jpg', 'restaurant_idx': 10},
        {'name': 'Шиш кебаб', 'description': 'Шашлик на шампурах', 'price': 98.0, 'weight': 310, 'image_url': 'https://i.pinimg.com/736x/ad/49/f8/ad49f89789847a5d27b55fc80e1587e0.jpg', 'restaurant_idx': 10},
        {'name': 'Лахмаджун', 'description': 'Турецька піца з м\'ясом', 'price': 85.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/1200x/81/f5/84/81f5842d8ff2081411edd83dc70ef095.jpg', 'restaurant_idx': 10},

        {'name': 'Філадельфія', 'description': 'Класичний рол з лососем', 'price': 185.0, 'weight': 240, 'image_url': 'https://i.pinimg.com/736x/e1/1b/83/e11b838229539c658deb28134ef7379c.jpg', 'restaurant_idx': 11},
        {'name': 'Каліфорнія', 'description': 'Рол з крабом та авокадо', 'price': 165.0, 'weight': 220, 'image_url': 'https://i.pinimg.com/1200x/2c/08/78/2c0878d152e77e2da1f704734987b714.jpg', 'restaurant_idx': 11},
        {'name': 'Сет Токіо', 'description': 'Асорті з різних ролів', 'price': 320.0, 'weight': 350, 'image_url': 'https://i.pinimg.com/1200x/83/d9/3c/83d93c96e48ec42f0458cfe683c89c3b.jpg', 'restaurant_idx': 11},
        {'name': 'Спайсі тун', 'description': 'Гострий рол з тунцем', 'price': 175.0, 'weight': 230, 'image_url': 'https://i.pinimg.com/1200x/50/00/d8/5000d85d3085b52aa06f95c576d5877b.jpg', 'restaurant_idx': 11},
        {'name': 'Дракон рол', 'description': 'Рол з вугрем та авокадо', 'price': 195.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/1200x/61/4f/97/614f9738df2016883d29a6df2021589d.jpg', 'restaurant_idx': 11},
        {'name': 'Сашімі лосось', 'description': 'Свіжий лосось нарізаний', 'price': 220.0, 'weight': 120, 'image_url': 'https://i.pinimg.com/1200x/2e/22/c8/2e22c8b20b519570a7dac039f8ca4cf6.jpg', 'restaurant_idx': 11},

        {'name': 'Рол майстра', 'description': 'Авторський рол від шефа', 'price': 195.0, 'weight': 260, 'image_url': 'https://i.pinimg.com/736x/21/05/49/210549b7a448ff111e19e5fe76947265.jpg', 'restaurant_idx': 12},
        {'name': 'Сет майстра', 'description': 'Преміум сет від шефа', 'price': 350.0, 'weight': 380, 'image_url': 'https://i.pinimg.com/736x/21/05/49/210549b7a448ff111e19e5fe76947265.jpg', 'restaurant_idx': 12},
        {'name': 'Червоний дракон', 'description': 'Рол з креветкою та авокадо', 'price': 185.0, 'weight': 240, 'image_url': 'https://i.pinimg.com/736x/20/10/4c/20104c61d2238c2f6bb95bf8399c41be.jpg', 'restaurant_idx': 12},
        {'name': 'Грін рол', 'description': 'Рол з огірком та авокадо', 'price': 155.0, 'weight': 200, 'image_url': 'https://i.pinimg.com/1200x/80/04/7e/80047efe629a8467ce527188cbed4959.jpg', 'restaurant_idx': 12},
        {'name': 'Темпура рол', 'description': 'Рол у темпурі з креветкою', 'price': 205.0, 'weight': 270, 'image_url': 'https://i.pinimg.com/736x/7e/00/73/7e0073925ae9064686b94710bf0ea3c9.jpg', 'restaurant_idx': 12},
        {'name': 'Нігірі сет', 'description': 'Асорті нігірі з різною рибою', 'price': 280.0, 'weight': 200, 'image_url': 'https://i.pinimg.com/1200x/70/80/7d/70807d0a752165771ea38c1b57b076d6.jpg', 'restaurant_idx': 12},

        {'name': 'Місо суп', 'description': 'Традиційний японський суп', 'price': 95.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/1200x/74/ea/51/74ea51b40b2b46827fc2692f093c7061.jpg', 'restaurant_idx': 13},
        {'name': 'Рамен класичний', 'description': 'Японська локшина з бульйоном', 'price': 125.0, 'weight': 400, 'image_url': 'https://i.pinimg.com/1200x/d2/6c/a7/d26ca7c688128542ebc5e9d491db1b6e.jpg', 'restaurant_idx': 13},
        {'name': 'Якіторі', 'description': 'Курячі шашлики на паличках', 'price': 110.0, 'weight': 180, 'image_url': 'https://i.pinimg.com/1200x/05/45/80/05458036394edf41c89fafdb83a9a1f9.jpg', 'restaurant_idx': 13},
        {'name': 'Теріякі курятина', 'description': 'Курка в соусі теріякі', 'price': 135.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/736x/39/6f/ad/396fad1ed606053cfac95dff4a1e0f0a.jpg', 'restaurant_idx': 13},
        {'name': 'Суші сет класичний', 'description': 'Асорті класичних суші', 'price': 240.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/736x/b1/21/41/b121419a4f6e16be30b58364b1b5681c.jpg', 'restaurant_idx': 13},
        {'name': 'Удон з овочами', 'description': 'Товста локшина з овочами', 'price': 115.0, 'weight': 350, 'image_url': 'https://i.pinimg.com/1200x/ea/e4/b5/eae4b57263f41856f1b16d267357d221.jpg', 'restaurant_idx': 13},

        {'name': 'Вок з куркою', 'description': 'Курка з овочами у воку', 'price': 98.0, 'weight': 320, 'image_url': 'https://i.pinimg.com/1200x/b4/ab/7d/b4ab7dd9b8a2bf621972460f83cdcfb9.jpg', 'restaurant_idx': 14},
        {'name': 'Вок з яловичиною', 'description': 'Яловичина з овочами у воку', 'price': 108.0, 'weight': 340, 'image_url': 'https://i.pinimg.com/1200x/b2/af/b3/b2afb3a5da4dd961d4cd538ef555376f.jpg', 'restaurant_idx': 14},
        {'name': 'Вок з креветками', 'description': 'Креветки з овочами у воку', 'price': 125.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/1200x/82/c0/79/82c079d4faf9a56b48cf91ee39238e6d.jpg', 'restaurant_idx': 14},
        {'name': 'Вок вегетаріанський', 'description': 'Овочі гриль у воку', 'price': 85.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/1200x/0e/48/39/0e4839fb5a5411a664d7d3bca514b6c3.jpg', 'restaurant_idx': 14},
        {'name': 'Вок мікс', 'description': 'Суміш м\'яса та морепродуктів', 'price': 135.0, 'weight': 360, 'image_url': 'https://i.pinimg.com/736x/b4/5e/6b/b45e6b0279a9d4fe55484650c2bd1069.jpg', 'restaurant_idx': 14},
        {'name': 'Вок з тофу', 'description': 'Тофу з овочами та соусом', 'price': 88.0, 'weight': 290, 'image_url': 'https://i.pinimg.com/736x/3b/33/57/3b3357e75c65a42570dc704fa77f45cc.jpg', 'restaurant_idx': 14},

        {'name': 'Кунг Пао курка', 'description': 'Класична китайська страва з куркою', 'price': 112.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/1200x/d2/ff/4c/d2ff4ca1299e9e82836be746e9a68958.jpg', 'restaurant_idx': 15},
        {'name': 'Солодко-кисла свинина', 'description': 'Свинина в солодко-кислому соусі', 'price': 118.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/1200x/f6/a3/d6/f6a3d694aa5fcaae78bb2954b4d9ea8a.jpg', 'restaurant_idx': 15},
        {'name': 'Локшина з овочами', 'description': 'Китайська локшина зі свіжими овочами', 'price': 95.0, 'weight': 320, 'image_url': 'https://i.pinimg.com/1200x/d6/90/55/d690555eaf7c7bf9de330586c31cb58d.jpg', 'restaurant_idx': 15},
        {'name': 'Печінка по-китайськи', 'description': 'Печінка з цибулею та соусом', 'price': 105.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/1200x/43/26/45/432645947dab378074e5acecdef06ab2.jpg', 'restaurant_idx': 15},
        {'name': 'Дім-сам сет', 'description': 'Асорті китайських пельменів', 'price': 135.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/736x/4c/5f/67/4c5f67cffd7d1d66afd0182683969903.jpg', 'restaurant_idx': 15},
        {'name': 'Рис з куркою', 'description': 'Смажений рис з куркою та овочами', 'price': 98.0, 'weight': 340, 'image_url': 'https://i.pinimg.com/736x/44/cd/09/44cd09f364351a195aaa683bbe8520df.jpg', 'restaurant_idx': 15},

        {'name': 'Омлет з беконом', 'description': 'Смачний омлет з хрустким беконом', 'price': 95.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/736x/a9/c3/6e/a9c36e795b0db69ddb430030a740c9b9.jpg', 'restaurant_idx': 16},
        {'name': 'Сирники', 'description': 'Домашні сирники зі сметаною', 'price': 88.0, 'weight': 220, 'image_url': 'https://i.pinimg.com/736x/de/a3/21/dea321603432c705cafdd656edcdecd3.jpg', 'restaurant_idx': 16},
        {'name': 'Вівсянка з фруктами', 'description': 'Смачна вівсянка зі свіжими фруктами', 'price': 75.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/736x/4d/30/8d/4d308d68352bb5f07fe05091043087c7.jpg', 'restaurant_idx': 16},
        {'name': 'Сніданок англійський', 'description': 'Яйця, бекон, ковбаски, боби', 'price': 125.0, 'weight': 380, 'image_url': 'https://i.pinimg.com/1200x/5b/97/a5/5b97a51cfed463ae07ea79301ee1719b.jpg', 'restaurant_idx': 16},
        {'name': 'Тост з авокадо', 'description': 'Хліб з авокадо та яйцем', 'price': 82.0, 'weight': 200, 'image_url': 'https://i.pinimg.com/736x/9f/e6/2a/9fe62a0d1671512f3be1379368ba37f6.jpg', 'restaurant_idx': 16},
        {'name': 'Млинці з ягодами', 'description': 'Свіжі млинці з ягодами та сиропом', 'price': 92.0, 'weight': 240, 'image_url': 'https://i.pinimg.com/1200x/12/10/7b/12107be9968c835b17d0e0c5cb9f0281.jpg', 'restaurant_idx': 16},

        {'name': 'Капучіно', 'description': 'Ароматна кава з молоком', 'price': 55.0, 'weight': 200, 'image_url': 'https://i.pinimg.com/736x/f8/56/1e/f8561ea80e14bd1989b4fe87736e1468.jpg', 'restaurant_idx': 17},
        {'name': 'Лате', 'description': 'Ніжний лате з молоком', 'price': 58.0, 'weight': 220, 'image_url': 'https://i.pinimg.com/736x/11/ef/d7/11efd75b7b3bb8fbfbbae1e582473691.jpg', 'restaurant_idx': 17},
        {'name': 'Сніданок континентальний', 'description': 'Випічка, масло, джем, кава', 'price': 95.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/736x/a4/d5/2c/a4d52c2ff29fcb9115d345586491647d.jpg', 'restaurant_idx': 17},
        {'name': 'Яйця Бенедикт', 'description': 'Яйця з голландським соусом', 'price': 115.0, 'weight': 300, 'image_url': 'https://i.pinimg.com/1200x/0e/ed/db/0eeddb5d759c6adab16cd12908755235.jpg', 'restaurant_idx': 17},
        {'name': 'Сендвіч з лососем', 'description': 'Свіжий лосось на хлібі', 'price': 125.0, 'weight': 250, 'image_url': 'https://i.pinimg.com/1200x/44/89/7f/44897f12c7e987c27b7c1dec194ea6c8.jpg', 'restaurant_idx': 17},
        {'name': 'Круасан з шоколадом', 'description': 'Свіжий круасан з шоколадом', 'price': 65.0, 'weight': 120, 'image_url': 'https://i.pinimg.com/1200x/34/a0/59/34a059a12664dcae118986a011cd897c.jpg', 'restaurant_idx': 17},

        {'name': 'Круасан класичний', 'description': 'Французький круасан з маслом', 'price': 58.0, 'weight': 100, 'image_url': 'https://i.pinimg.com/1200x/aa/3a/1f/aa3a1f33f9c99a4b2c27981dc362a368.jpg', 'restaurant_idx': 18},
        {'name': 'Круасан з мигдалем', 'description': 'Круасан з мигдальною начинкою', 'price': 68.0, 'weight': 120, 'image_url': 'https://i.pinimg.com/736x/ae/e6/3f/aee63f06d902054010cd8dcf53fabb37.jpg', 'restaurant_idx': 18},
        {'name': 'Круасан з джемом', 'description': 'Круасан з фруктовим джемом', 'price': 62.0, 'weight': 110, 'image_url': 'https://i.pinimg.com/736x/53/e6/3b/53e63bd562e64eba395f8e541d7fece4.jpg', 'restaurant_idx': 18},
        {'name': 'Еклер', 'description': 'Французький еклер з кремом', 'price': 75.0, 'weight': 90, 'image_url': 'https://i.pinimg.com/1200x/84/73/50/847350f384a5244190de55711e7695b6.jpg', 'restaurant_idx': 18},
        {'name': 'Макарон', 'description': 'Французькі макарони різних смаків', 'price': 85.0, 'weight': 100, 'image_url': 'https://i.pinimg.com/1200x/80/70/72/8070726a678ffa3e9f085d528aad7d3f.jpg', 'restaurant_idx': 18},
        {'name': 'Бріош', 'description': 'Французька випічка бріош', 'price': 65.0, 'weight': 130, 'image_url': 'https://i.pinimg.com/736x/d7/e9/99/d7e99948412384571729673b4042dc8d.jpg', 'restaurant_idx': 18},

        {'name': 'Багель з лососем', 'description': 'Свіжий багель з лососем', 'price': 95.0, 'weight': 220, 'image_url': 'https://i.pinimg.com/736x/2c/eb/58/2ceb58a23db7d485ee37aa7fea36ead8.jpg', 'restaurant_idx': 19},
        {'name': 'Хліб на заквасці', 'description': 'Домашній хліб на заквасці', 'price': 45.0, 'weight': 400, 'image_url': 'https://i.pinimg.com/1200x/c2/f0/59/c2f059cbcae0ad599a48d39e873c5ecf.jpg', 'restaurant_idx': 19},
        {'name': 'Брі з медом', 'description': 'Французький сир брі з медом', 'price': 88.0, 'weight': 180, 'image_url': 'https://i.pinimg.com/1200x/25/66/dc/2566dccdff774c08be1dfcbe00305147.jpg', 'restaurant_idx': 19},
        {'name': 'Квасоля з ковбасою', 'description': 'Французька квасоля з ковбасою', 'price': 105.0, 'weight': 320, 'image_url': 'https://i.pinimg.com/1200x/61/13/c3/6113c35d952c1606c9faef8368dc1078.jpg', 'restaurant_idx': 19},
        {'name': 'Тарт з яблуками', 'description': 'Французький тарт з яблуками', 'price': 78.0, 'weight': 200, 'image_url': 'https://i.pinimg.com/1200x/6b/71/e7/6b71e767f047396ef90fdbe5bc9f6675.jpg', 'restaurant_idx': 19},
        {'name': 'Круасан з сиром', 'description': 'Круасан з сирною начинкою', 'price': 65.0, 'weight': 115, 'image_url': 'https://i.pinimg.com/1200x/0c/f8/e7/0cf8e78f1152fad958976832bf2ae62c.jpg', 'restaurant_idx': 19},

        {'name': 'Торт шоколадний', 'description': 'Ніжний шоколадний торт', 'price': 185.0, 'weight': 600, 'image_url': 'https://i.pinimg.com/736x/9d/25/93/9d2593780fe22eba7acf1ea6e9e57110.jpg', 'restaurant_idx': 20},
        {'name': 'Чізкейк', 'description': 'Класичний чізкейк', 'price': 165.0, 'weight': 500, 'image_url': 'https://i.pinimg.com/1200x/a1/cf/56/a1cf56db16d6d2d53465dbece6d86d62.jpg', 'restaurant_idx': 20},
        {'name': 'Тірамісу', 'description': 'Італійський десерт тірамісу', 'price': 145.0, 'weight': 280, 'image_url': 'https://i.pinimg.com/1200x/24/1f/40/241f40cdb81ee38b3d1e87a593c5ace7.jpg', 'restaurant_idx': 20},
        {'name': 'Торт полуничний', 'description': 'Торт зі свіжими полуницями', 'price': 175.0, 'weight': 550, 'image_url': 'https://i.pinimg.com/1200x/7f/b5/b0/7fb5b072c979caa4604099d29859cf3b.jpg', 'restaurant_idx': 20},
        {'name': 'Еклери', 'description': 'Асорті еклерів', 'price': 95.0, 'weight': 200, 'image_url': 'https://i.pinimg.com/736x/15/6e/dd/156edd2b6a8cf32069e197219e5ae2d9.jpg', 'restaurant_idx': 20},
        {'name': 'Торт червоний оксамит', 'description': 'Торт червоний оксамит', 'price': 195.0, 'weight': 580, 'image_url': 'https://i.pinimg.com/1200x/1e/92/70/1e92708d4c30a0c225cd6e2a8d6aac8b.jpg', 'restaurant_idx': 20},

        {'name': 'Торт на замовлення', 'description': 'Авторський торт на замовлення', 'price': 350.0, 'weight': 1000, 'image_url': 'https://i.pinimg.com/736x/9d/25/97/9d259789b163c4a1340ff9171b257743.jpg', 'restaurant_idx': 21},
        {'name': 'Торт весільний', 'description': 'Розкішний весільний торт', 'price': 450.0, 'weight': 1200, 'image_url': 'https://i.pinimg.com/1200x/6d/bf/3e/6dbf3e7038fab81d2c285f32547af34e.jpg', 'restaurant_idx': 21},
        {'name': 'Торт дітям', 'description': 'Яскравий торт для дітей', 'price': 280.0, 'weight': 800, 'image_url': 'https://i.pinimg.com/736x/b2/c2/29/b2c22964c3757bb8d59818852f9624a3.jpg', 'restaurant_idx': 21},
        {'name': 'Торт ювілейний', 'description': 'Торт для святкування', 'price': 320.0, 'weight': 900, 'image_url': 'https://i.pinimg.com/1200x/02/19/51/0219512cca7f6dbad9f3920aa70097e4.jpg', 'restaurant_idx': 21},
        {'name': 'Торт з макаронами', 'description': 'Торт прикрашений макаронами', 'price': 295.0, 'weight': 750, 'image_url': 'https://i.pinimg.com/1200x/5a/d4/c7/5ad4c74b9b0eacb3dc698ed63b86769b.jpg', 'restaurant_idx': 21},
        {'name': 'Торт з квітами', 'description': 'Торт з квітковою прикрасою', 'price': 380.0, 'weight': 950, 'image_url': 'https://i.pinimg.com/1200x/fb/98/be/fb98be094a6b3fc5fe2601e6709b644d.jpg', 'restaurant_idx': 21},

    ]

    for rest_idx, rest_data in enumerate(restaurants_data):
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
        db.commit()
        db.refresh(restaurant)
        for dish in [d for d in dishes_data if d['restaurant_idx'] == rest_idx]:
            db.add(models.Dish(
                name=dish['name'],
                description=dish['description'],
                price=dish['price'],
                weight=dish['weight'],
                image_url=dish['image_url'],
                restaurant_id=restaurant.id
            ))
        db.commit()
        print(f"Додано 6 унікальних страв у ресторан: {restaurant.name}")
    
    # Створюємо адміністратора
    admin_user = models.Users(
        username="administrator",
        email="admin@example.com",
        hashed_password=crypt.hash("admin123"),
        is_admin=1
    )
    db.add(admin_user)
    print("Додано адміністратора: administrator / admin@example.com / admin123")
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
