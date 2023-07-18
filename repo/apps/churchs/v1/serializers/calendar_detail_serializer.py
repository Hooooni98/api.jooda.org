from rest_framework import serializers
from apps.churchs.models import ChurchCalendar


class ChurchCalendarDetailSerializer(serializers.ModelSerializer):
    church_calendar_id = serializers.SerializerMethodField()
    church_id = serializers.SerializerMethodField()

    class Meta:
        model = ChurchCalendar
        fields = (
            "church_calendar_id",
            "church_id",
            "title",
            "content",
            "start_date",
            "end_date",
        )

    def get_church_calendar_id(self, obj):
        return obj.id

    def get_church_id(self, obj):
        return obj.church.id
