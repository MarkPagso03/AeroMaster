from import_export import resources
from .models import Question, Student
from AeroMaster_admin.models import ExamResult, UserFeedback, faculty




class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        exclude = ('id',)  # 💡 This tells Django NOT to expect 'id'
        import_id_fields = ('text',)
        fields = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer',
                  'subject')  # Adjust this as per your model fields


class UserResource(resources.ModelResource):
    class Meta:
        model = Student
        exclude = ('id',)  # 💡 This tells Django NOT to expect 'id'
        import_id_fields = ('email',)
        search_fields = ('first_name', 'last_name', 'email')
        fields = ('first_name', 'middle_initial', 'last_name', 'id_number', 'email', 'password')


class ExamResultResource(resources.ModelResource):
    class Meta:
        model = ExamResult
        exclude = ('id',)  # 💡 This tells Django NOT to expect 'id'
        import_id_fields = ('student_id',)
        fields = ('student_id', 'aero_result', 'math_result', 'struc_result', 'acrm_result', 'pwrp_result',
                  'eemle_result', 'percent_result', 'total_result')


class UserFeedbackResource(resources.ModelResource):
    class Meta:
        model = UserFeedback
        exclude = ('id',)  # 💡 This tells Django NOT to expect 'id'
        import_id_fields = ('student_id',)
        fields = ('student_id', 'aero_satisfaction', 'aero_comments', 'math_satisfaction', 'math_comments',
                  'struc_satisfaction', 'struc_comments', 'acrm_satisfaction', 'acrm_comments', 'pwrp_satisfaction',
                  'pwrp_comments', 'eemle_satisfaction', 'eemle_comments')


class FacultyResource(resources.ModelResource):
    class Meta:
        model = faculty
        import_id_fields = ('emp_id',)  # unique field used to match records on import
        fields = (
            'id',
            'first_name',
            'last_name',
            'emp_id',
            'email',
            'password',
        )
