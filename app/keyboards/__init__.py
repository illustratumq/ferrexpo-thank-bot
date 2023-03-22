from dataclasses import dataclass


@dataclass()
class Admin:
    statistic: str = 'Статистика 📊'
    rating: str = 'Рейтинг 🏆'
    delete: str = 'Видатити користувача 🚫'
    update: str = 'Оновити користувачів 🔄'


@dataclass()
class Auth:
    authorization: str = 'Шукати 🔍'


@dataclass()
class Menu:
    send_points: str = 'Віддати подяку 📬'
    my_profile: str = 'Мій профіль 💚'
    rules: str = 'Правила 📃'
    info: str = 'Цікаві матеріали про вдячність'
    user_rating: str = 'Рейтинг 🏆'
    go_next: list = 'Так 🥰', 'Йес 🫡', 'Оце магія! Звідки знаєш? 🤩'
    history: str = 'Моя історія 📚'
    main_menu: str = 'В головне меню ↩'
    my_send: str = 'Мої перекази ✉'
    to_me_send: str = 'Перекази для мене 📩'
    back_to_history: str = '⬅ Назад'
    auth_bt: str = 'Авторизуватись ✔'
    share_phone: str = 'Поділитися телефоном 📲'

    auth: Auth = Auth()


class Send:
    select_user: str = 'Список колег'
    confirm: str = 'Так, відправити ✅'
    values: list = ['Порядність', 'Відповідальність', 'Ініціатива', 'Різноманітність', 'Інновації']
    custom_value: str = 'Свій варіант'
    next_button = '✅ Відправити wellcoin-и'


@dataclass
class Buttons:
    menu = Menu()
    send = Send()
    admin = Admin()
