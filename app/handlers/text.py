from dataclasses import dataclass

from app.config import Config


@dataclass
class Authorization:
    config = Config.from_env()

    auth_method_email = (
        f'Для старту треба ідентифікувати тебе через робочу пошту 📩\n\n'
        f'Натисни на кнопку "Пошук 🔍", для швидкого пошуку пошти, або відправ текстове повідомлення.'
    )

    auth_method_phone = (
        f'Для старту треба ідентифікувати тебе через робочій телефон.\n\n'
        f'Натисни кнопку "Пошук 🔍", для швидкого пошуку телефону, або відправ номер текстовим повідомленням.\n\n'
        f'Ти також можеш швидко поділитися савоїм номером натиснувши кнопку нижче.'
    )

    auth_method = auth_method_phone if config.misc.auth_method == "Phone" else auth_method_email

    authorization_cmd = (
        f'Вітаємо тебе у просторі Вдячності! 👋\n\n'
        f'Я чат-бот Wellbeing Company, буду твоїм корисним помічником та допоможу тобі:\n'
        f'✅ швидко та зручно відправити твої теплі слова колегам\n'
        f'✅ розподіляти та рахувати wellcoin-и 💚\n'
        f'✅ отримувати подяки від співробітників за твої добрі вчинки\n'
        f'✅ отримувати корисну інформацію та практики для підтримки себе у ресурсному стані 😎\n\n'
        f'{auth_method if config.misc.auth_method == "Email" else ""}'
    )


@dataclass
class Text:
    auth = Authorization()
