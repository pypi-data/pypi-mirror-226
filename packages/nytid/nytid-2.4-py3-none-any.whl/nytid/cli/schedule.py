import datetime
from enum import Enum
import ics.icalendar
import logging
import typer
from typing_extensions import Annotated

from nytid.cli import courses as coursescli
from nytid import courses as courseutils
from nytid import schedules as schedutils

cli = typer.Typer(name="schedule", help="Working with course schedules")


def update_end_date(start, end):
    """
    Returns a correct end date.
    """
    if end < start:
        return start + datetime.timedelta(weeks=1)
    return end


start_date_opt = typer.Option(help="The start date", formats=["%Y-%m-%d"])
end_date_opt = typer.Option(help="The end date", formats=["%Y-%m-%d"])


class GroupByDayOrWeek(str, Enum):
    week = "week"
    day = "day"


group_by_day_or_week = typer.Option(
    help="Choose whether to group events " "by day or week", case_sensitive=False
)


@cli.command()
def show(
    course: Annotated[str, coursescli.course_arg_regex] = ".*",
    register: Annotated[str, coursescli.register_opt_regex] = coursescli.MINE,
    start: Annotated[datetime.datetime, start_date_opt] = str(datetime.date.today()),
    end: Annotated[datetime.datetime, end_date_opt] = str(
        datetime.date.today() + datetime.timedelta(weeks=1)
    ),
    group_by: Annotated[GroupByDayOrWeek, group_by_day_or_week] = "week",
):
    """
    Shows schedule for courses in human readable format.
    """
    end = update_end_date(start, end)
    registers = coursescli.registers_regex(register)
    the_courses = list(coursescli.courses_regex(course, registers))

    schedule = ics.icalendar.Calendar()

    for a_course, a_register in the_courses:
        try:
            course_conf = courseutils.get_course_config(a_course, a_register)
        except KeyError as err:
            logging.error(f"Can't find {a_course} in {a_register}: {err}")
            continue

        try:
            course_ics_url = course_conf.get("ics")
        except KeyError as err:
            logging.error(f"Can't find schedule URL for {a_course}: {err}")
            continue

        course_schedule = schedutils.read_calendar(course_ics_url)

        schedule.events.update(course_schedule.events)
    first = True
    if group_by == GroupByDayOrWeek.week:
        group_by_idx = 1
    elif group_by == GroupByDayOrWeek.day:
        group_by_idx = 2
    for event in schedule.timeline:
        if event.end.date() < start.date():
            continue
        elif event.begin.date() > end.date():
            continue
        if first:
            first = False
            current_epoc = event.begin.isocalendar()[group_by_idx]
        elif event.begin.isocalendar()[group_by_idx] != current_epoc:
            print("\n")
            current_epoc = event.begin.isocalendar()[group_by_idx]

        print(schedutils.format_event_short(event))
