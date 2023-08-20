from .examon_item_registry import ExamonItemRegistry
from .models.question_factory import QuestionFactory


def examon_item(internal_id=None, choices=None, repository=None,
                tags=None, hints=None, param1=None, version=1):
    def inner_function(function):
        processed_question = QuestionFactory.build(
            function=function, choice_list=choices, repository=repository,
            tags=tags, hints=hints, internal_id=internal_id,
            version=version, param1=param1, metrics=True)
        ExamonItemRegistry.add(processed_question)
        return function

    return inner_function
