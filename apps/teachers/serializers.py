from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        # import ipdb;ipdb.set_trace()
        if 'content' in attrs and attrs['content']:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')

        if 'state' in attrs:
            if attrs['state'] == 'SUBMITTED':
                raise serializers.ValidationError('Teacher cannot set state to SUBMITTED')
        
        if 'student' in attrs and attrs['student']:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')
        
        if self.instance.teacher != attrs["teacher"]:
            raise serializers.ValidationError('Teacher cannot grade for other teacher''s assignment')

        if self.instance.state == "DRAFT":
            raise serializers.ValidationError('SUBMITTED assignments can only be graded')

        if self.instance.state == "GRADED":
            raise serializers.ValidationError('GRADED assignments cannot be graded again')
            
        if self.partial:
            return attrs

        return super().validate(attrs)