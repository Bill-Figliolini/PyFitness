from typing import override
from django.db import models
from django.db.models.fields import BooleanField, TextField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

# Create your models here.


class Exercise(models.Model):
    """
    Class which represents the data model of the basic Exercises users will select from.

    Attributes:
        name (Charfield): Represents the row that stores the name of the exercise
        category (IntegerField): Represents the category of the exercise, as defined in ExerciseCategory
    """

    class ExerciseCategory(models.IntegerChoices):
        STRENGTH_CHEST = 0
        STRENGTH_BACK = 1
        STRENGTH_ARMS = 2
        STRENGTH_ABDOMINALS = 3
        STRENGTH_LEGS = 4
        STRENGTH_SHOULDERS = 5
        AEROBIC = 6
        FLEXIBILITY = 7

    name = models.CharField(max_length=100)
    category = models.IntegerField(choices=ExerciseCategory)

    @override
    def __str__(self) -> str:
        return self.name


# TODO: Current implementation of Record implies that there should be immutable. Needs more thought.
class ExercisePlan(models.Model):
    """
    Class that represents the list of exercises that the user wants to perform.

    Attributes:
        exercises: Many-to-Many relation over Exercise
    """

    exercises = models.ManyToManyField(to=Exercise)


# TODO: active/inprogress field?
class ScheduledExercise(models.Model):
    """
    Class that represents the scheduling of a future Exercise plan

    Attributes:
        datetime: When the User wants to schedule the exercise for
        plan: ForeignKey to an ExercisePlan
    """

    datetime = models.DateTimeField()
    plan = models.ForeignKey(to=ExercisePlan, on_delete=models.SET_NULL)

    @override
    def __str__(self) -> str:
        return f"Exercise {self.plan} at {self.datetime}"

    def has_expired(self) -> bool:
        return self.datetime < timezone.now()


# TODO: Considerations for later: Addition of Completed bool field
class Record(models.Model):
    """
    Class representing Past exercise plans.

    Attributes:
        exercise_plan: Stored ForeignKey to the scheduled_exercise that was done
        missed: boolean for tracking if exercise was missed, initialized to true
        text: User commentary on their exercise, initialized to the entry string
    Methods:
        make_record(): takes an exercise_plan, and makes a record entry
        edit_missed(): inverts missed
        edit_text(): replaces text with input

    """

    scheduled_plan: ForeignKey[ScheduledExercise] = models.ForeignKey(
        to=ScheduledExercise, on_delete=models.PROTECT
    )
    text: TextField[str] = models.TextField()
    missed: BooleanField = models.BooleanField()

    @override
    def __str__(self) -> str:
        return f"Record for {self.scheduled_plan} with text {self.text} that was missed={self.missed}"


class UserAccount(models.Model):
    """
    Class for handling the Database potion of userdata.

    Attributes:
        saved_plans: exercise plans stored by the user
        scheduled_plans: Planned exercises, that will expire at the time they are scheduled
        record: Records of the user's past exercises
    Methods:
        make_plan(): Takes in a list of Exercise entries and assembles an ExercisePlan in saved_plans
        remove_plan(): removes entry from saved_plans, if it exists
        schedule_plan(): takes a datetime and a ExercisePlan and creates a ScheduledExercise
        unschedule_plan(): removes entry from scheduled_plans, if it exists
        edit_record_text(): Edits the text field on a record entry
        edit_record_missed(): Inverts the status of the missed field on a record entry
    """
