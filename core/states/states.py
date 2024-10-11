from aiogram.fsm.state import State, StatesGroup


class StateRandomTask(StatesGroup):
    CHECK_ANSWER = State()
    NEXT_TASK = State()


class StateSpecificTask(StatesGroup):
    TASK_SELECTED = State()
    CHECK_ANSWER = State()
    NEXT_TASK = State()


class StateTest(StatesGroup):
    TASK_SELECTED = State()
    CHECK_ANSWER = State()
    NEXT_TASK = State()
    TEST_END = State()
    CHECK_SOLVE = State()


class StateRandomVar(StatesGroup):
    CHECK_ANSWER = State()
    NEXT_TASK = State()
    VAR_END = State()
    CHECK_SOLVE = State()


class StateChangeName(StatesGroup):
    CHANGE_NAME = State()

class StateChangeAvatar(StatesGroup):
    CHANGED_AVATAR = State()


class StateWeeklyVar(StatesGroup):
    CHECK_ANSWER = State()
    NEXT_TASK = State()

class StateRegisterUser(StatesGroup):
    IDENT_PURPOSE = State()

class StateAdminAddTask(StatesGroup):
    ADD_TASK = State()
    ADD_ANSWER = State()
    NEXT_ADD = State()

class StateAdminAddQuset(StatesGroup):
    ADD_QUEST = State()

class StateDailyQuests(StatesGroup):
    REVIEW_QUESTS = State()
    CHESK_QUESTS = State()