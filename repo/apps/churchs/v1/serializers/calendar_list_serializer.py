from rest_framework import serializers
from apps.churchs.models import ChurchCalendar
from datetime import date


class ChurchCalendarListSerializer(serializers.ModelSerializer):
    church_calendar_id = serializers.SerializerMethodField()
    is_current_month = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = ChurchCalendar
        fields = (
            "church_calendar_id",
            "title",
            "content",
            "start_date",
            "end_date",
            "is_current_month",
        )

    def get_church_calendar_id(self, obj):
        return obj.id

    def get_is_current_month(self, obj):
        if (
            self.context["month"] == obj.start_date.month
            or self.context["month"] == obj.end_date.month
        ):
            return True
        else:
            return False

    def get_end_date(self, obj):
        if obj.start_date == obj.end_date:
            return ""
        else:
            return obj.end_date
