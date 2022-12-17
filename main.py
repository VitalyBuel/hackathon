import csv
import random
from random import shuffle
from itertools import cycle


# Копируем информацию из таблицы
with open("it-dictionary.csv", "r", encoding="utf8") as csvfile:
    data = csv.DictReader(csvfile, delimiter="/", quotechar=" ")
    events = {x["event"]: [x["word"], x['difficulty'], x['alternative'], x['alternative2'], x['hint']] for x in data}

# with open('Data.json', encoding='utf8') as f:
#     words = json.loads(f.read())['test']  # массив из словарей слов


right = ['Отлично!', 'Правильно!', 'Супер!', 'Точно!', 'Верно!', 'Хорошо!', 'Неплохо!']

wrong = ['Ой!', 'Не то!', 'Ты ошибся!', 'Немного не то!', 'Неверно!', 'Неправильно!', 'Ошибочка!']

_next = ['Далее', 'Следующий вопрос', 'Продолжим', 'Следующее', 'Едем дальше!']

wtf = ['Прости, не понимаю тебя', 'Можешь повторить, пожалуйста?', 'Повтори, пожалуйста', 'Прости, не слышу тебя']

goodbye = ['Пока!', 'До встречи!', 'Будем на связи!', 'Рада была пообщаться!', 'Пока-пока!']

hey = ['Привет', 'Приветствую тебя', 'Отличный день сегодня', 'Хорошо, что мы снова встретились', 'Приветик',
       'Здравствуй']

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
    if request.is_new_session:
        user_storage = {}
        response.set_text(
            f'{random.choice(hey)}!\n'
            'Это навык “Разговорник на айтишном".\n'  
            'В форме игры ты узнаешь слова из айти-сферы!\n  '
            'Ты готов начать?'
        )
        response.set_buttons(
            [
                {'title': 'да', 'hide': True},
                {'title': 'нет', 'hide': True},
                {'title': 'помощь', 'hide': True}
            ]
        )
        # response.set_analytics(
        #     [
        #         {'name': 'начало диалога'}
        #     ]
        # )

        return response, user_storage

# Обрабатываем ответы пользователя.
    elif request.command.lower() == 'подсказка':
        # Подсказка если пользователь затрудняется ответить.
        buttons = user_storage['buttons']
        response.set_text(user_storage["hint"])
        response.set_buttons(buttons)

        return response, user_storage

    elif request.command.lower() == 'помощь':
        # Помощь, которая показывает как работает диалог.
        response.set_text("Я помогаю тебе проверить твое знание слов из ИТ сферы в формате викторины.\n Начнем?")
        user_storage = {}
        response.set_buttons(
            [
                {'title': 'да', 'hide': True},
                {'title': 'нет', 'hide': True}
            ]
        )

        return response, user_storage

    elif request.command.lower() == 'нет':
        # Если в начале диалога пользователь отказывается продолжать, тогда завершаем сессию.
        response.set_text(f"Спасибо за игру! {random.choice(goodbye)}!")
        response.set_end_session(True)
        user_storage = {}

        return response, user_storage

    else:
        if request.command.lower() in ['да', '', ''] and 'choice' not in user_storage.keys():
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

            return response, user_storage

        elif request.command.lower() == user_storage["answer"]:
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

        elif request.command.lower() == "не знаю":
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

            return response, user_storage

        elif request.command.lower() == "конец игры":
            # Если в любом месте диалог пользователь не хочет продолжать, выводим результат пользователя.
            # Завершаем сессию.
            response.set_text("Спасибо за игру!\n Правильных ответов: {}\n".format(user_storage["right_answers"])
                    + "До встречи!")
            response.set_end_session(True)
            user_storage = {}

            return response, user_storage


        # Команда которая отрабатывает если Алиса не поняла что сказал пользователь.
        # else:
        #     response.set_text(random.choice(wtf))
        #     #response.set_buttons(
        #     #     [
        #     #         {'title': 'да', 'hide': True},
        #     #         {'title': 'нет', 'hide': True},
        #     #         {'title': 'помощь', 'hide': True}
        #     #     ]
        #     # )
        #
        #     return response, user_storage

        buttons = user_storage['buttons']
        question = user_storage['event']

        response.set_buttons(buttons)
        response.set_text(f"{random.choice(wrong)}! Попробуй еще раз.\n{question}")
        return response, user_storage



