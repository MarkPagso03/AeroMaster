from import_export import resources
from .models import Question, User


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        exclude = ('id',)  # 💡 This tells Django NOT to expect 'id'
        import_id_fields = ('text',)
        fields = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'subject')  # Adjust this as per your model fields


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('id',)  # 💡 This tells Django NOT to expect 'id'
        import_id_fields = ('email',)
        fields = ('first_name', 'middle_initial', 'last_name', 'id_number', 'email', 'password')
