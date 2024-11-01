LEXICON: dict[str, str] = {
    '/start': 'Начинается регистрация',
    '/solve': 'РЕШАТЬ!',
    '/backpack': 'Мой рюкзак',
    '/help': 'Помощь'
}

LEXICON_COMMANDS: dict[str, str] = {
    '/menu': 'Главное меню',
    '/solve': 'Решать!',
    '/backpack': 'Рюкзак',
    '/room': 'Комната',
    '/quests': 'Квесты',
    '/leaders': 'Рейтинг',
    '/shop': 'Магазин',
    '/info': 'Информация',
}

LEXICON_POINTS: dict[str, int] = {
    'random_task_plus': 2,
    'random_task_minus': -1,
    'daily_task_plus': 5,
    'daily_task_minus': -1,
}

LEXICON_MEDIA: dict[str, str] = {
    'my_backpack': './media/my_backpack.png',
    'category_request': './media/admin/category_request.png',
    'no_photo_request': './media/admin/no_photo_request.png',
    'info_sub': './media/info_sub.png',
}

LEXICON_STICKERS: dict[str, str] = {
    'open_case': 'CAACAgIAAxkBAAEM2yRm8DLUVYwe06wYvGFkDsDbRo3n8gACDAADFm5MEphNRY1LQz4fNgQ',
    'transfer': 'CAACAgIAAxkBAAEM4Vhm9FmNqCKirMmgKiihEjyi46gcsQACIgADFm5MEk3fueVj-TT0NgQ',
    'info': 'CAACAgIAAxkBAAEM4Vhm9FmNqCKirMmgKiihEjyi46gcsQACIgADFm5MEk3fueVj-TT0NgQ',
    'payment': 'CAACAgIAAxkBAAEM8FNnBXD-hmW29Zr_91ftXA4avh_aiAACCAADFm5MEiqXqMzgotLQNgQ',
    'score5': 'CAACAgIAAxkBAAEM8dFnB9KvjfEyBS257LmRqD0Neqd17AACBwADFm5MEvFIqhFf1OndNgQ',
    'score4': 'CAACAgIAAxkBAAEM8dNnB9K_-P7s0Kergf-Dkmo6V3xL_wACAgADFm5MEsIltIZB6z7VNgQ',
    'score3': 'CAACAgIAAxkBAAEM8dVnB9LOlm8eGHvcJjS9M01t3eW61QACsQoAAv3GqUrCleapCKIvyTYE',
    'score2': 'CAACAgIAAxkBAAEM8ddnB9LVdqIspKSxpU_0IAGmDRg_agAC1AwAAmSX0Unr2bjSVr0jRTYE',
    'score1': 'CAACAgIAAxkBAAEM8dlnB9L6Nd7cxokQ3yGW2YOCctDTKAAC7A0AAuYXuEiesWAOv_9-BzYE',
    'score0': 'CAACAgIAAxkBAAEM8dtnB9MC3kj_Ck6jnB-uyr87SmlghAACpwoAAhsViErJQuPFqV7QJjYE',
}

LEXICON_BUTTON_main_menu: dict[str, str] = {
    'events': '☄️ Ивенты [СКОРО]',
    'solve': '🧑🏽‍💻 РЕШАТЬ!',
    'quests': '🕹 Квесты',
    'my_backpack': '🎒 Мой рюкзак',
    'shop': '🏪 Магазин',
    'my_room': '🏠 Моя комната',
    'info': '📊 Информация',
    'table_leaders': '🏆 Рейтинг',
}

LEXICON_BUTTON_solve_menu: dict[str, str] = {
    'solve_daily_task': '☀️ Задание дня',
    'solve_tasks': '🔢 Все задания',
    'solve_variant': '📖 Решать вариант',
    'solve_theory': '📚 Теория',
    'solve_simulators': '🏋️‍♀️ Тренажёры [СКОРО]',
}

LEXICON_BUTTON_back_menu: dict[str, str] = {
    'back_menu': '↩️ В меню',
    'back_room': '↩️ В комнату',
    'back_solve': '↩️ Назад',
    'back_info': '↩️ В Информация',
}

LEXICON_BUTTON_theory_menu: dict[str, str] = {
    'theory_tasks': '🔢 По заданиям',
    'theory_topic': '🔡 По темам',
}


LEXICON_BUTTON: dict[str, str] = {
    'solve': '🧑🏽‍💻 РЕШАТЬ!',
    'solve_tasks': '🔢 Все задания',
    'random_task': '🎲 Случайное задание',
    'specific_task': '✍️ Прорешать задание',
    'test': '📝 Пройти тест по заданию',
    'test_start': '▶️ Начать тест',
    'solve_variant': '📖 Решать вариант',
    'random_variant': "🎲 Cлучайный вариант",
    'random_variant_start': '▶️ Решать случайный вариант',
    'weekly_variant': '📅 Еженедельный вариант',
    'weekly_variant_start': '▶️ Решать eженедельный вариант',
    'solve_daily_task': '☀️ Задание дня',
    'events': '☄️ Ивенты [СКОРО]',
    'solve_simulators': '🏋️‍♀️ Тренажёры [СКОРО]',
    'solve_theory': '📚 Теория',
    'theory_tasks': '🔢 По заданиям',
    'theory_topic': '🔡 По темам',

    'begin_solve': '▶️ Начать решение',
    'resolve_task': '🔄 Перерешать',
    'check_solution': '🔍 Смотреть решение',
    'next_task': '⏩ Следующее задание',
    'view_results': '⏩ Смотреть результаты',

    'quests': '🕹 Квесты',
    'daily_bonus': '💫 Ежедневный бонус',
    'collect_daily_bonus': '☑️ Собрать ежедневный бонус',
    'quests_daily': '⭐️ Ежедневные квесты',
    'quests_check': '🔍 Проверить выполнение квестов',
    'quests_other': '✨ Другие квесты',

    'my_backpack': '🎒 Мой рюкзак',

    'shop': '🏪 Магазин',
    'shop_cases': '🎁 Полка с кейсами',
    'shop_leaders': '🦸🏼‍♂️ Уголок лидера',
    'shop_sub': '💎 Подписка',

    'my_room': '🏠 Моя комната',
    'stats_for_tasks': '🧾 Статистика по заданиям',

    'room_settings': '⚙️ Настройки',
    'change_name': '🔧 Изменить имя',
    'change_purpose': '💯 Изменить цель по баллам',

    'info': '📊 Информация',
    'info_sub': '💎 О подписке',
    'invite_friends': '🤝 Пригласить друга',
    'help': '✨ Помощь',
    'report_error': '❕ Сообщить об ошибке',
    'faq': '❔ Часто задаваемые вопросы (FAQ)',
    'ask_question': '❔ Задать свой вопрос',


    'back_menu': '↩️ В меню',
    'back_room': '↩️ В комнату',
    'back_solve': '↩️ Назад',
    'back': '↩️ Назад',
    'back_info': '↩️ В Информация',

    'table_leaders': '🏆 Рейтинг',

    'purpose_1': 'до 70 баллов',
    'purpose_2': '70-85 баллов',
    'purpose_3': '85-95 баллов',
    'purpose_4': '95+ баллов',

    'backpack_avatars': '👾 Аватары',
    'backpack_cases': '🎁 Кейсы',
    'backpack_other': '🧩 Предметы',

    'prev': '⬅️',
    'next': '➡️',

    'admin_panel': '🦸🏽 Админ-панель',


    'admin_stats': '🔬 Cтатистика',

    'admin_users': '👶🏼 Пользователи',

    'admin_edit': '🔧 Добавить/Изменить',
    'admin_add_task': '🔖 Добавить задание',
    'admin_edit_task': '✏️ Изменить задание',
    'admin_add_var': '📙 Добавить вариант',
    'admin_add_quest': '🕹 Добавить квест',

    'admin_send': '📩 Рассылка',

    'admin_request': '📩 Обращения',
    'admin_new_request': 'Новые',
    'admin_finished_request': 'Завершенные',

    'back_type': 'Другие категории',
    'answer_user': 'Ответить пользователю',
    'mark_spam': 'Это спам',
    'mark_finished': 'Закрыть обращение',

    'back_admin_request': '↩️ В Обращения',
    'back_admin_panel': '↩️ В Админ-панель',

    'admin_add_task_next': '➕ Добавить еще',
}

LEXICON_BUTTON_UTC: dict[str, str] = {
    'utc_2': 'МСК-1 (Калининградское)',
    'utc_3': 'МСК (Московское)',
    'utc_4': 'МСК+1 (Самарское)',
    'utc_5': 'МСК+2 (Екатеринбургское)',
    'utc_6': 'МСК+3 (Омское)',
    'utc_7': 'МСК+4 (Красноярское)',
    'utc_8': 'МСК+5 (Иркутское)',
    'utc_9': 'МСК+6 (Якутское)',
    'utc_10': 'МСК+7 (Владивостокское)',
    'utc_11': 'МСК+8 (Магаданское)',
    'utc_12': 'МСК+9 (Камчатское)',
}

LEXICON_CREATE_IMAGE_TASK: dict[str, str] = {
    'link': 't.me/math1ege_bot',
    'name': 'БОТ-ТРЕНАЖЁР | ЕГЭ МАТЕМАТИКА',
}
