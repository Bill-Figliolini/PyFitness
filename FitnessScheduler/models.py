from django.db import models


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


class ExercisePlan(models.Model):
    """
    Class that represents the list of exercises that the user wants to perform.

    Attributes:
        exercises: Many-to-Many relation over Exercise
    """

    exercises = models.ManyToManyField(to=Exercise)


class ScheduledExercise(models.Model):
    """
    Class that represents the scheduling of a future Exercise plan

    Attributes:
        datetime: When the User wants to schedule the exercise for
        plan: ForeignKey to an ExercisePlan
    """

    datetime = models.DateTimeField()
    plan = models.ForeignKey(to=ExercisePlan, on_delete=models.SET_NULL)


class Record(models.Model):
    """
    Class representing Past exercise plans.

    Attributes:
        exercise_plan: Stored ForeignKey to the exercise_plan that was done
        datetime: When the Exercise was performed
        text: User commentary on their exercise
    """

    exercise_plan = models.ForeignKey(to=ExercisePlan, on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    text = models.TextField()
