import csv
from random import shuffle
from itertools import cycle


with open("it-dictionary.csv", "r", encoding="utf8") as csvfile:
    data = csv.DictReader(csvfile, delimiter=",", quotechar=" ")
    events = {x["event"]: [x["word"], x['difficulty']] for x in data}


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        user_storage = {}
        response.set_text('Выберите сложность')
        response.set_buttons([{'title': 'easy', 'hide': True}, {'title': 'medium', 'hide': True},
                             {'title': 'hard', 'hide': True}])

        return response, user_storage

    else:
        # Обрабатываем ответ пользователя.
        if request.command.lower() == "конец игры":
            response.set_text("Спасибо за игру!\n Правильных ответов: {}\n".format(user_storage["right_answers"])
                              + "До встречи!")
            response.set_end_session(True)
            user_storage = {}

            return response, user_storage

        elif request.command.lower() in ['easy', 'medium', 'hard'] and "level" not in user_storage.keys():
            user_storage['level'] = request.command.lower()
            _a = list(filter(lambda x: request.command.lower() == events[x][1], events.keys()))
            shuffle(_a)
            inf_list = cycle(_a)
            user_storage['questions'] = inf_list

            event = next(user_storage['questions'])
            word = events[event][0]
            buttons = get_random_buttons(word)

            user_storage["event"] = event
            user_storage["answer"] = word
            user_storage["buttons"] = buttons
            user_storage["right_answers"] = 0
            response.set_text('Я буду говорить значение слова, а тебе нужно угадать что это.\n'
                              'Если захочешь остановить игру, скажи "конец игры".\n'
                              'Первый вопрос: {}'.format(user_storage["event"]))
            response.set_buttons(user_storage["buttons"])

            return response, user_storage

        elif request.command.lower() == user_storage["answer"]:
            # Пользователь ввел правильный вариант ответа.
            event = next(user_storage['questions'])
            word = events[event][0]
            buttons = get_random_buttons(word)
            user_storage["event"] = event
            user_storage["answer"] = word
            user_storage["buttons"] = buttons
            user_storage["right_answers"] += 1
            response.set_text('Верно!\n'
                              'Следующий вопрос. Что означает: {}'.format(user_storage["event"]))
            response.set_buttons(user_storage["buttons"])

            return response, user_storage

        buttons = get_random_buttons(user_storage['answer'])

        response.set_buttons(buttons)
        response.set_text("Неверно! Попробуй еще раз.")

        return response, user_storage



# def get_random_buttons(date):
#     dates = list(range(int(date) - 200, int(date) + 200))
#     dates.pop(dates.index(int(date)))
#     shuffle(dates)
#
#     dates = dates[:3]
#     dates.append(date)
#     shuffle(dates)
#     buttons = [{'title': str(date), 'hide': True} for date in dates]
#
#     return buttons


if __name__ == '__main__':
    handle_dialog()
