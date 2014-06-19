from django import forms
from school_calendar.models import *
from school_calendar.widgets import *
from school_calendar.fields import *
from dateutil import rrule

DAY_CHOICES = (
    (MO,"Monday"),
    (TU,"Tuesday"),
    (WE,"Wednesday"),
    (TH,"Thursday"),
    (FR,"Friday" ),
    (SA,"Saturday"),
    (SU,"Sunday"),
)

class RecurrenceRuleForm(forms.ModelForm):
    params = RecurrenceRuleParamsField(
        label="Recurrence", 
        required=False, 
        widget=RecurrenceRuleParamsWidget(
            [
                forms.CheckboxSelectMultiple(choices=DAY_CHOICES),
                SelectDateWidget(),
            ]
       )
    )
    class Meta:
        model = RecurrenceRule
        exclude = ('name',)

class EventForm(forms.ModelForm):
    startdatetime = forms.SplitDateTimeField(label="Start Date/Time", required=True, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    enddatetime = forms.SplitDateTimeField(label="End Date/Time", required=False, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    class Meta:
        model = Event
        exclude = ('school','attendees','creator','rule')

class CourseSessionForm(EventForm):
    class Meta:
        model = Event
        exclude = ('name','course','school','attendees','creator','rule')

class CourseSessionRecurrenceForm(forms.Form):
    startdatetime = forms.SplitDateTimeField(label="Start Date/Time", required=True, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    enddatetime = forms.SplitDateTimeField(label="End Date/Time", required=False, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    allday = forms.BooleanField(label="All Day", required=False)
    recurring = forms.BooleanField(label="Recurring", required=False)
    frequency = forms.ChoiceField(label="Frequency", required=False, choices=FREQUENCY_CHOICES)
    byweekday = forms.MultipleChoiceField(label="Recurrence Days", required=False, choices=DAY_CHOICES, widget=forms.CheckboxSelectMultiple())