# так как у меня нет таблиц в бд для этих значений, я храню их как константы
# да и нафиг нужны для них отдельные таблицы


FUEL_TYPES = [
    "Gasoline",
    "Diesel",
    "Hybrid",
    "Electric",
]

BODY_TYPES = [
    'Convertible',
    'Coupe',
    'Hatchback',
    'SUV',
    'Minivan',
    'Sedan',
    'Pickup'
]

# списки кортежей для форм (ChoiceField)

BODY_TYPE_CHOICES = [
    ('Convertible', 'Convertible'),
    ('Coupe', 'Coupe'),
    ('Hatchback', 'Hatchback'),
    ('SUV', 'SUV'),
    ('Minivan', 'Minivan'),
    ('Sedan', 'Sedan'),
    ('Pickup', 'Pickup'),
]

FUEL_TYPE_CHOICES = [
    ('Gasoline', 'Gasoline'),
    ('Diesel', 'Diesel'),
    ('Hybrid', 'Hybrid'),
    ('Electric', 'Electric'),
]

TRANSMISSION_TYPES = [
    ('Manual', 'Manual'),
    ('Automatic', 'Automatic'),
]