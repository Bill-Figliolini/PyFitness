from datetime import datetime
from typing import override
from django.db import models
from django.db.models.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    TextField,
)
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone

from accounts.models import UserAccount

import django_stubs_ext

django_stubs_ext.monkeypatch()


class ExerciseCategory(models.Model):
    name: CharField[str] = CharField(max_length=100)

    @override
    def __str__(self) -> str:
        return self.name


class Exercise(models.Model):
    """
    Class which represents the data model of the basic Exercises users will select from.

    Attributes:
        name (Charfield): Represents the row that stores the name of the exercise
        category (IntegerField): Represents the category of the exercise, as defined in ExerciseCategory
    """

    name: CharField[str] = models.CharField(max_length=100)
    category: ForeignKey[ExerciseCategory] = models.ForeignKey(
        to=ExerciseCategory, on_delete=models.PROTECT
    )

    @override
    def __str__(self) -> str:
        return "self.name -> self.category"


class ExercisePlanHolder(models.Model):
    """
    Class that represents the list of exercises that the user wants to perform.

    Attributes:
        exercises: Many-to-Many relation over Exercise
    """

    id: IntegerField[int] = models.IntegerField(primary_key=True)
    name: TextField[str] = models.TextField()
    owner: ForeignKey[UserAccount] = models.ForeignKey(
        to=UserAccount, on_delete=models.CASCADE
    )
    dateCreated: DateTimeField[datetime] = models.DateTimeField()
    ordered_exercises: ManyToManyField[ExercisePlan, Exercise] = models.ManyToManyField(
        to=Exercise, through="ExercisePlan", related_name="holder"
    )

    @override
    def __str__(self) -> str:
        return f"{self.name}- Owner: {self.owner.name}, created: {self.dateCreated}"


class ExercisePlan(models.Model):
    """
    Class of enumerated exercises that ExercisePlanHolder is built upon
    """

    holder: ForeignKey[ExercisePlanHolder] = models.ForeignKey(
        to=ExercisePlanHolder, on_delete=models.CASCADE
    )
    exercise: ForeignKey[Exercise] = models.ForeignKey(
        to=Exercise, on_delete=models.PROTECT
    )
    order: models.PositiveIntegerField[int] = models.PositiveIntegerField()

    class Meta:
        unique_together: tuple[str, str] = ("holder", "order")
        ordering: list[str] = ["order"]

    @override
    def __str__(self) -> str:
        return f"{self.holder.name}, {self.exercise.name}, {self.order}"


class ScheduledExercise(models.Model):
    """
    Class that represents the scheduling of a future Exercise plan

    Attributes:
        datetime: When the User wants to schedule the exercise for
        plan: ForeignKey to an ExercisePlan
        completed: has been marked completed
    """

    id: IntegerField[int] = models.IntegerField(primary_key=True)
    scheduledtime: DateTimeField[datetime] = models.DateTimeField()
    owner: ForeignKey[UserAccount] = models.ForeignKey(
        to=UserAccount, on_delete=models.CASCADE
    )
    plan: ForeignKey[ExercisePlanHolder] = models.ForeignKey(
        to=ExercisePlanHolder, on_delete=models.PROTECT
    )

    completed: BooleanField[bool] = models.BooleanField()

    @override
    def __str__(self) -> str:
        return (
            f"Exercise {self.plan.name} for {self.owner.name} at {self.scheduledtime}"
        )

    def has_expired(self) -> bool:
        return self.scheduledtime < timezone.now()


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

    id: IntegerField[int] = models.IntegerField(primary_key=True)
    scheduled_plan: ForeignKey[ScheduledExercise] = models.ForeignKey(
        to=ScheduledExercise, on_delete=models.PROTECT
    )
    owner: ForeignKey[UserAccount] = models.ForeignKey(
        to=UserAccount, on_delete=models.CASCADE
    )
    text: TextField[str] = models.TextField()
    missed: BooleanField[bool] = models.BooleanField()

    @override
    def __str__(self) -> str:
        return (
            f"Record {self.scheduled_plan}  with text {self.text}. Missed={self.missed}"
        )
