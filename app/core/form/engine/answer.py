
from app.core.form.models.answer import FormAnswer
from app.core.form.status import AnswerStatus
from app.core.user import User


class AnswerElement:
    def __init__(self, label, answer):
        self.label = label
        self.answer = answer


class BaseFormAnswer:
    def __init__(self, base, answer_id):
        self._base = base
        self._answer_id = answer_id
        self.__map = list(self.__get().items())
        self.__cursor = 0

    @property
    def label(self):
        return self._base.label

    @property
    def id(self):
        return self._answer_id

    @property
    def status(self):
        return self.model.status

    @property
    def human_date(self):
        return self.model.human_date

    def get_user_answers(self, limit: int = 10):
        from app.core.form.engine import FormEngine

        user_answers = FormAnswer.get_all_user_answers(self.model.user, limit=limit)
        last_answers = []
        for answer in user_answers:
            base = FormEngine.get_from_technical_name(answer.form_technical_name)
            answer_form = BaseFormAnswer(base=base, answer_id=answer.id)

            if answer_form.id == self.id:
                continue

            last_answers.append(BaseFormAnswer(base=base, answer_id=answer.id))
        return last_answers

    @property
    def model(self) -> FormAnswer:
        try:
            answer_model: FormAnswer = FormAnswer.get_from_id(self._answer_id)
        except ValueError:
            raise RuntimeError("Unknown answer")

        return answer_model

    def __get(self) -> dict[str, any]:
        answer_model = self.model

        if answer_model.form_technical_name != self._base.technical_name:
            raise RuntimeError("FormAnswer model of another object")

        answer_data_class = self._base.dataclass.parse_obj(answer_model.form_data)
        answer_map = dict()
        for field_technical_name, filed_human_name in self._base.fields_map.items():
            name = filed_human_name
            answer = getattr(answer_data_class, field_technical_name, "Ошибка при загрузке")
            answer_map[name] = answer

        return answer_map

    def __iter__(self):
        return self

    def __next__(self) -> AnswerElement:
        try:
            current_element_raw = self.__map[self.__cursor]
        except IndexError:
            raise StopIteration()
        self.__cursor += 1
        return AnswerElement(*current_element_raw)


class BaseFormAnswerController:
    def __init__(self, form_base):
        self._base = form_base

    def get_all_answer_in_user(self, user: User) -> list[BaseFormAnswer]:
        models = FormAnswer.query.filter(FormAnswer.form_technical_name == self._base.technical_name,
                                         FormAnswer.user_id == user.id).limit(10).all()
        return [BaseFormAnswer(self._base, answer.id) for answer in models]

    def get_all_forms_in_status(self, status: AnswerStatus, limit: int = 500):
        models = FormAnswer.query.filter(FormAnswer.form_technical_name == self._base.technical_name,
                                         FormAnswer.processed_status == status.value).order_by(
            FormAnswer.id.desc()).limit(limit).all()
        return [BaseFormAnswer(self._base, answer.id) for answer in models]

    def get_from_id(self, answer_id):
        return BaseFormAnswer(self._base, answer_id)
