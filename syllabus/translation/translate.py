from modeltranslation.translator import register, TranslationOptions

from syllabus.models import CourseSyllabusTest, TestQuestion


@register(CourseSyllabusTest)
class CourseSyllabusTestTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(TestQuestion)
class TestQuestionTranslationOptions(TranslationOptions):
    fields = ("question",)