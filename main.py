import csv
import random
from random import shuffle
from itertools import cycle

frequency = 10
start = []
close = []
_help = []
what_can_you_do = []
dont_know = []

# Копируем информацию из таблицы
with open("it-dictionary.csv", "r", encoding="utf8") as csvfile:
    data = csv.DictReader(csvfile, delimiter="/", quotechar=" ")
    events = {x["event"]: [x["word"], x["difficulty"], x["alternative"], x["alternative2"], x["hint"]] for x in data}

with open("answer.csv", "r", encoding="utf8") as csvfile:
    answer = csv.DictReader(csvfile, delimiter=",", quotechar=" ")
    answers = {x["answer"]: [x["var1"], x["var2"], x["var3"], x["var4"], x["var5"]] for x in answer}

with open('simantics.csv', 'r', encoding="utf8") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        start += row[::frequency]
        close += row[1::frequency]
        _help += row[2::frequency]
        what_can_you_do += row[3::frequency]
        dont_know += row[4::frequency]

right = ['Отлично!', 'Правильно!', 'Супер!', 'Точно!', 'Верно!', 'Хорошо!', 'Неплохо!', 'Именно так!']

wrong = ['Ой!', 'Не то :(!', 'Ошибка :(!', 'Немного не то!', 'Неверно!', 'Неправильно!', 'Ошибочка!']

_next = ['Далее', 'Следующий вопрос', 'Продолжим', 'Следующее', 'Едем дальше!']

wtf = ['Прости, не понимаю тебя!', 'Можешь повторить, пожалуйста?', 'Повтори, пожалуйста!', 'Прости, не слышу тебя!']

goodbye = ['Пока!', 'До встречи!', 'Будем на связи!', 'Рада была пообщаться!', 'Пока-пока!']

hey = ['Привет', 'Приветствую тебя', 'Отличный день сегодня', 'Хорошо, что мы снова встретились!', 'Приветик!',
       'Здравствуй!']

do_not_know = ["Жаль!",
               "Эх, жалко!",
               "Мы это исправим!",
               "Ничего, все ещё впереди!",
               "Потренируйся ещё немного!",
               "Попробуй в следующий раз!",
               "Практикой можно достичь совершенства!",
               "Эту тему стоит подучить.",
               "Запоминай!",
               "В следующий раз получится!",
               "Поднажми, все супер!",
               "Ничего, бывает :)",
               "Бывает :)",
               "Все окей :)",
               "Старайся!",
               "Тренируйся дальше!"]


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    # Если новая сессия тогда возвращаем приветствие.
    if request.is_new_session or request.command.lower() in start:
        user_storage = {}
        response.set_text(
            f'{random.choice(hey)}!\n'
            'Это навык “Разговорник на айтишном".\n'  
            'В форме игры ты узнаешь слова из айти-сферы!\n  '
            'Для начала выбери сложность. Легко, нормально или сложно?\n'
        )
        response.set_buttons(
            [
                {'title': 'easy', 'hide': True},
                {'title': 'medium', 'hide': True},
                {'title': 'hard', 'hide': True},
            ]
        )

        response.set_image(
            {
                "type": "BigImage",
                "image_id": "1533899/b692acca8dacc02c2ecb",
                "description": f'{random.choice(hey)}!\nЭто навык “Разговорник на айтишном".\n'
                               'В форме игры ты узнаешь слова из айти-сферы!\n'
                               'Для начал выбери сложность.\n',
            }
        )

        return response, user_storage

    # Обрабатываем ответы пользователя.
    elif request.command.lower() == 'подсказка':
        # Подсказка если пользователь затрудняется ответить.
        buttons = user_storage['buttons']
        response.set_text(user_storage["hint"])
        response.set_buttons(buttons)
        response.set_analytics(
            [

                {
                    "name": "подсказка",
                    "value": {
                        "слово": user_storage["answer"],
                    }
                }
            ]
        )

        return response, user_storage

    elif request.command.lower() in what_can_you_do:
        response.set_text("Я помогаю тебе проверить твое знание слов из ИТ сферы в формате викторины.\n\n"
                          "Я могу задавать вопросы и анализировать Ваши ответы.\n\n"
                          "Оценивать Ваши знания в зависимости от результатов игры\n\n"
                          "Больше информации Вы узнаете воспользовавшись командой - 'ПОМОЩЬ'\n\n"
                          "Продолжим или нет?")
        user_storage = {}
        response.set_buttons(
            [
                {'title': 'продолжить', 'hide': True},
                {'title': 'нет', 'hide': True}
            ]
        )

        return response, user_storage

    elif request.command.lower() in _help:
        # Помощь, которая показывает как работает диалог.
        if 'choice' not in user_storage.keys():
            response.set_text("Вы всегда можете обратится за помощью с помощью команды - 'ПОМОЩЬ'.\n\n"
                              "Если у Вас возникли трудности с ответом на вопрос вы можете вызвать - 'ПОДСКАЗКУ'\n\n"
                              "Если захотите пропустить вопрос воспользуйтесь командой - 'НЕ ЗНАЮ'\n\n"
                              "Чтобы завершить игру используйте команду - 'КОНЕЦ ИГРЫ'\n\n"
                              "Начнем? Да или нет?")
            user_storage = {}
            response.set_buttons(
                [
                    {'title': 'да', 'hide': True},
                    {'title': 'нет', 'hide': True}
                ]
            )

        else:
            response.set_text("Вы всегда можете обратится за помощью с помощью команды - 'ПОМОЩЬ'.\n\n"
                              "Если у Вас возникли трудности с ответом на вопрос вы можете вызвать - 'ПОДСКАЗКУ'\n\n"
                              "Если захотите пропустить вопрос воспользуйтесь командой - 'НЕ ЗНАЮ'\n\n"
                              "Чтобы завершить игру используйте команду - 'КОНЕЦ ИГРЫ'\n\n"
                              "Продолжить или нет?")
            user_storage = {}
            response.set_buttons(
                [
                    {'title': 'продолжить', 'hide': True},
                    {'title': 'нет', 'hide': True}
                ]
            )

        return response, user_storage

    elif request.command.lower() == 'нет':
        # Если в начале диалога пользователь отказывается продолжать, тогда завершаем сессию.
        response.set_text(f"Спасибо за игру! {random.choice(goodbye)}!")
        response.set_end_session(True)
        user_storage = {}
        response.set_analytics(
            [
                {
                    "name": "начало игры",
                    "value": {
                        "выбор": request.command.lower(),
                    }
                }
            ]
        )

        return response, user_storage

    elif request.command.lower() not in ['easy', 'medium', 'hard'] \
            and 'choice' not in user_storage.keys():
        response.set_text("Для начала Вам нужно выбрать сложность!\n")
        response.set_buttons(
            [
                {'title': 'easy', 'hide': True},
                {'title': 'medium', 'hide': True},
                {'title': 'hard', 'hide': True},
            ]
        )
        response.set_analytics(
            [
                {
                    "name": "Начало игры",
                    "value": {
                        "действие": "не выбрана сложность",
                        "произнес": request.command.lower(),
                    }
                }
            ]
        )

        return response, user_storage

    else:
        if request.command.lower() in ['easy', 'medium', 'hard'] and 'choice' \
                not in user_storage.keys():
            # Генерируем первый вопрос.
            user_storage['choice'] = request.command.lower()
            _a = list(filter(lambda x: request.command.lower() == events[x][1], events.keys()))
            shuffle(_a)
            inf_list = cycle(_a)
            user_storage['questions'] = inf_list

            event = next(user_storage['questions'])
            word = events[event][0]
            alternative = events[event][2]
            alternative2 = events[event][3]
            hint = events[event][4]
            buttons = [
                {'title': word, 'hide': True},
                {'title': alternative, 'hide': True},
                {'title': alternative2, 'hide': True},
                {'title': 'не знаю', 'hide': True},
                {'title': 'подсказка'}
            ]

            user_storage["event"] = event
            user_storage["answer"] = word
            user_storage["buttons"] = buttons
            user_storage["right_answers"] = 0
            user_storage["hint"] = hint
            response.set_text(
                'Я буду говорить значение слова, а тебе нужно угадать что это.\n'
                'Если захочешь остановить игру, скажи "конец игры".\n\n'
                'Первый вопрос:\n {}'.format(user_storage["event"])
            )

            response.set_buttons(user_storage["buttons"])
            response.set_analytics(
                [
                    {
                        "name": "начало игры",
                        "value": {
                            "выбор": request.command.lower(),
                        }
                    }
                ]
            )

            return response, user_storage

        elif request.command.lower() == user_storage["answer"] \
                or request.command.lower() in answers[user_storage["answer"]]:
            # Пользователь ввел правильный вариант ответа.
            event = next(user_storage['questions'])
            word = events[event][0]
            alternative = events[event][2]
            alternative2 = events[event][3]
            hint = events[event][4]
            buttons = [
                {'title': alternative, 'hide': True},
                {'title': word, 'hide': True},
                {'title': alternative2, 'hide': True},
                {'title': 'не знаю', 'hide': True},
                {'title': 'подсказка'}
            ]

            user_storage["event"] = event
            user_storage["answer"] = word
            user_storage["buttons"] = buttons
            user_storage["right_answers"] += 1
            user_storage["hint"] = hint

            response.set_text(
                f'{random.choice(right)}!\n\n'
                f'{random.choice(_next)}:\n {user_storage["event"]}'
            )
            response.set_buttons(user_storage["buttons"])

            return response, user_storage

        elif request.command.lower() == 'не знаю' or request.command.lower() in dont_know:
            # Пользователь не знает ответ.
            event = next(user_storage['questions'])
            word = events[event][0]
            alternative = events[event][2]
            alternative2 = events[event][3]
            hint = events[event][4]
            buttons = [
                {'title': alternative, 'hide': True},
                {'title': alternative2, 'hide': True},
                {'title': word, 'hide': True},
                {'title': 'не знаю', 'hide': True},
                {'title': 'подсказка'}
            ]

            user_storage["event"] = event
            user_storage["answer"] = word
            user_storage["buttons"] = buttons
            user_storage["right_answers"] += 0
            user_storage["hint"] = hint

            response.set_text(
                f'{random.choice(do_not_know)}!\n'
                f'Правильный ответ - {user_storage["answer"]}\n\n'
                f'{random.choice(_next)}:\n {user_storage["event"]}'
            )
            response.set_buttons(user_storage["buttons"])

            response.set_analytics(
                [
                    {
                        "name": "не знаю",
                        "value": {
                            "выбор": request.command.lower(),
                            "слово": user_storage["answer"],
                        }
                    }
                ]
            )

            return response, user_storage

        elif request.command.lower() in close:
            # Если в любом месте диалог пользователь не хочет продолжать, выводим результат пользователя.
            # Завершаем сессию.
            response.set_text("Спасибо за игру!\n Правильных ответов: {}\n".format(user_storage["right_answers"])
                              + "До встречи!")
            response.set_end_session(True)
            user_storage = {}

            response.set_analytics(
                [
                    {
                        "name": "конец игры",
                        "value": {
                            "произнес": request.command.lower(),
                        }
                    }
                ]
            )

            return response, user_storage

        buttons = user_storage['buttons']
        question = user_storage['event']

        response.set_buttons(buttons)
        response.set_text(f"{random.choice(wrong)}! Попробуй еще раз.\n{question}")
        response.set_analytics(
            [
                {
                    "name": "нераспознанный ответ",
                    "value": {
                        "произнес": request.command.lower(),
                    }
                }
            ]
        )

        return response, user_storage






