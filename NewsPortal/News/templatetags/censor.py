from django import template
import re

register = template.Library()

FORBIDDEN_WORDS = []  # Запрещенные слова


@register.filter()
def censor(text):
    if type(text) is str:
        for i in text.split():
            word = re.sub('\.|,|-|=|/|_|!|', '', i)
            if word.lower() in FORBIDDEN_WORDS:
                text = text.replace(i[1:len(word)], '*' * (len(word) - 1))
        return text
    else:
        raise 'Этот фильтр можно применять только к переменным строкового типа'


