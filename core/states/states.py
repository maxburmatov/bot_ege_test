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

class StateWeeklyVar(StatesGroup):
    CHECK_ANSWER = State()
    NEXT_TASK = State()

class StateRegisterUser(StatesGroup):
    IDENT_PURPOSE = State()
    IDENT_UTC = State()

class StateAdminAddTask(StatesGroup):
    ADD_TASK = State()
    ADD_ANSWER = State()

class StateAdminEditTask(StatesGroup):
    CHECK_TASK = State()
    ADD_TASK = State()
    ADD_ANSWER = State()

class StateAdminAddQuset(StatesGroup):
    ADD_QUEST = State()

class StateDailyTask(StatesGroup):
    TASK_SELECTED = State()
    CHECK_ANSWER = State()
    END_DAILY_TASK = State()

class StateRequestError(StatesGroup):
    REQUEST_ERROR = State()

class StateRequestQuestion(StatesGroup):
    REQUEST_QUESTION = State()

class StateAdminRequestAnswer(StatesGroup):
    REQUEST_ANSWER = State()

class StateAdminAddPointsAllBots(StatesGroup):
    ADD_POINTS = State()
