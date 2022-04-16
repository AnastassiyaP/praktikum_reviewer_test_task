import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        """
        Во-первых, если ты хочешь разбить на строки однострочную
        конструкцию, то разбиение должно содержать какие-то смысловые
        единицы. Например, одно условное выражение "not date" у тебя
        оказалось разнесено на две строчки. Также условное выражение
        лучше не отрывать от if, в остальном возможны варианты.

        Например, как можно написать:
        self.date = (
            dt.datetime.now().date() if not date
            else dt.datetime.strptime(date, '%d.%m.%Y').date())

        Или:
        self.date = (dt.datetime.now().date()
                     if not date
                     else
                     dt.datetime.strptime(date, '%d.%m.%Y').date())
        Во-вторых, всегда, когда это возможно, лучше переписать условие
        if без not. Это проще для восприятия.
        Как-то так:
        self.date = (
                     dt.datetime.strptime(date, '%d.%m.%Y').date()) if date
                     else dt.datetime.now().date())
        А вообще, если хочется перенести однострочную конструкцию,
        скорее всего, полное выражение будет читаемее:
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date())
        else:
            self.date = dt.datetime.now().date())
        """
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        """
        Название переменной Record с большой буквы, во-первых, перекрывает
        имя класса. Во-вторых, противоречит PEP8
        """
        for Record in self.records:
            """
            Здесь в цикле вызывается функция dt.datetime.now().date().
            Это не очень хорошо с точки зрения производительности, и
            метод может вернуть разные значения на разных этапах цикла.
            Лучше вызов функции сохранить в переменную перед циклом
            """
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            """
            Это условие сложно читается, и тут несколько причин:
            1. Вычисляемое выражение, которое используется больше
             одного раза, лучше сохранить в переменную days.
            2. Проще для восприятия, когда сравнение идет сначала
             с меньшей величиной, затем с большей:
                if days >=0 and days < 7:
            3. Но в данном случае питон позволяет упростить еще больше
             и создать цепочку сравнений:
                if 0 <= (today - record.date).days < 7
            """
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            """
            Переносы по \ запрещены правилами,
            а для f-строк перенос вообще не нужен.
            """
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        """
        else здесь не нужен
        """
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    """
    Цитата из задания: Метод get_today_cash_remained(currency) денежного
    калькулятора должен принимать на вход код валюты: одну из строк "rub",
    "usd" или "eur". Аргументы USD_RATE и EURO_RATE - лишние.
    И если бы они тут были нужны, их бы стоило делать в нижнем регистре.
    """
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        """
        Ты присваиваешь currency_type значение currency и потом
        переопределяешь ее для всех значимых значений usd,eur,rub.
        Если передать в качестве currency что-то еще(uah), то метод
        вернет, что остались uah, что некорректно. Надо либо возвращать
        в качестве значения по умолчанию рубли, либо создавать исключение.
        """
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            """
            Зачем это здесь?
            """
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        """
        Здесь не надо писать elif, поскольку остался единственный
        возможный вариант, то return надо делать из тела метода
        """
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    """
    Этот метод, во-первых, не нужен, т.к не добавляет нового
    функционала. Во вторых он с ошибкой, без return значение
    родительского метода возвращено не будет
    """
    def get_week_stats(self):
        super().get_week_stats()
