#!/usr/bin/env python3

"""
Helpers widely used in the application.
"""

import datetime
import typing

import click


def get_time_difference(
    start_date: datetime.datetime, end_date: datetime.datetime
) -> tuple[int, int]:
    """
    Return time difference between two dates as a (hours, seconds) tuple.
    """

    seconds_per_hour = 3600
    seconds_per_minute = 60

    seconds = (end_date - start_date).total_seconds()

    hours = int(seconds // seconds_per_hour)
    minutes = int(seconds % seconds_per_hour // seconds_per_minute)

    return hours, minutes


def print_with_alignment(title: str, value: str, width: int = 15) -> None:
    """
    Prints a string with an alignment given.
    """

    title = f"{title}:".ljust(width)

    print(f"{title} {value}")


def get_active_fast(
    fasts: list[dict[str, datetime.datetime | int]]
) -> dict[str, typing.Any] | None:
    """
    Return data of the active fast.
    """

    return fasts[-1] if len(fasts) > 0 and fasts[-1].get("stopped") is None else None


def is_fast_stopped(fast: dict[str, datetime.datetime | int]) -> bool:
    """
    Determines whether a fast is over or not.
    """

    return fast.get("stopped") is not None


def is_fast_completed(fast: dict[str, typing.Any]) -> bool:
    """
    Checks if a fast completed.
    """

    hours_in_fast = get_fast_length(fast)[0]
    fast_length = fast["length"] if fast["length"] is not None else 0

    return int(fast_length) <= hours_in_fast


def get_fast_length(fast: dict[str, typing.Any]) -> tuple[int, int]:
    """
    Returns length of a fast as a (hours, seconds) tuple.
    """

    started = fast["started"]
    stopped = fast.get("stopped")

    if stopped is not None:
        result = get_time_difference(started, stopped)
    else:
        result = 0, 0

    return result


def title_and_value(title: str, value: str, width: int = 15) -> str:
    """
    Aligns title & value by a given position.
    """

    if len(title) > width:
        width = len(title)

    title = f"{title}:".ljust(width)

    return f"{title} {value}"


def print_fast(fast: dict[str, typing.Any]) -> None:
    """
    Prints information about a fast.
    """

    time = fast["stopped"] if is_fast_stopped(fast) else datetime.datetime.now()
    goal = fast["started"] + datetime.timedelta(hours=fast["length"])

    __echo_fast_title(fast)
    click.echo()

    __echo_fast_from(fast)
    __echo_fast_goal(fast, goal)
    click.echo()

    __echo_fasting_zones(fast, time)
    click.echo()

    __echo_fast_progress_bar(fast, goal, time)
    click.echo()

    __echo_fast_elapsed_time(fast, time)

    if time <= goal:
        __echo_fast_remaining_time(time, goal)
    else:
        __echo_fast_extra_time(time, goal)


def __echo_fast_title(fast: dict[str, typing.Any]) -> None:
    if is_fast_stopped(fast):
        if is_fast_completed(fast):
            click.echo(click.style(text="COMPLETED FAST", bold=True, fg="green"))
        else:
            click.echo(click.style(text="FAILED FAST", bold=True, fg="red"))
    else:
        click.echo(click.style(text="ACTIVE FAST", bold=True, fg="yellow"))


def __echo_fast_from(fast: dict[str, typing.Any]) -> None:
    value = __get_day(fast["started"])
    value = title_and_value("From", value, 5)

    click.echo(value)


def __echo_fast_goal(fast: dict[str, typing.Any], goal: datetime.datetime) -> None:
    length = fast["length"]
    goal_string = __get_day(goal)
    goal_string = f"{goal_string} ({length} hours)"
    goal_string = title_and_value("Goal", goal_string, 5)

    click.echo(goal_string)


def __echo_fast_elapsed_time(
    fast: dict[str, typing.Any], time: datetime.datetime
) -> None:
    date1 = fast["started"]
    date2 = time if fast.get("stopped") is None else fast["stopped"]

    value = __get_time_difference(date1, date2)
    value = title_and_value("Elapsed time", value, 15)

    click.echo(str(value))


def __echo_fast_extra_time(time: datetime.datetime, goal: datetime.datetime) -> None:
    value = __get_time_difference(goal, time) if time >= goal else ""
    value = title_and_value(title="Extra time", value=value, width=15)

    click.echo(str(value))


def __echo_fast_remaining_time(
    time: datetime.datetime, goal: datetime.datetime
) -> None:
    value = (
        __get_time_difference(time - datetime.timedelta(minutes=1), goal)
        if time < goal
        else ""
    )

    value = title_and_value("Remaining", value, 15)

    click.echo(str(value))


def __line_for_zone(
    note: str,
    time: datetime.datetime,
    title: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime | None,
) -> str:
    zone_from = f"from {__get_day(start_time)}"

    if end_time is None:
        zone_note = note if start_time <= time else ""
    else:
        zone_note = note if start_time <= time < end_time else ""

    zone_note = title_and_value(f"{title}", f"{zone_from}{zone_note}")

    return str(zone_note)


def __echo_fasting_zones(fast: dict[str, typing.Any], time: datetime.datetime) -> None:
    note = " <-- you were here" if is_fast_stopped(fast) else " <-- you are here"

    anabolic_zone = fast["started"]
    catabolic_zone = anabolic_zone + datetime.timedelta(hours=4)
    fat_burning_zone = catabolic_zone + datetime.timedelta(hours=12)
    ketosis_zone = fat_burning_zone + datetime.timedelta(hours=8)
    deep_ketosis_zone = ketosis_zone + datetime.timedelta(hours=48)

    click.echo("Fasting zones:")
    click.echo("")

    line = __line_for_zone(note, time, "1. Anabolic", anabolic_zone, catabolic_zone)
    click.echo(line)

    line = __line_for_zone(note, time, "2. Catabolic", catabolic_zone, fat_burning_zone)
    click.echo(line)

    line = __line_for_zone(note, time, "3. Fat burning", fat_burning_zone, ketosis_zone)
    click.echo(line)

    line = __line_for_zone(note, time, "4. Ketosis", ketosis_zone, deep_ketosis_zone)
    click.echo(line)

    line = __line_for_zone(note, time, "5. Anabolic", deep_ketosis_zone, None)
    click.echo(line)


def __echo_fast_progress_bar(
    fast: dict[str, typing.Any], goal: datetime.datetime, time: datetime.datetime
) -> None:
    seconds_now = (time - fast["started"]).total_seconds()
    seconds_all = (goal - fast["started"]).total_seconds()

    percent = round(seconds_now / seconds_all * 100, 1)

    done_len = int(percent // 2.5)
    done_len = min(done_len, 40)

    left_len = int(40 - done_len)

    left = "-" * left_len
    done = "#" * done_len
    tail = str(percent)

    click.echo(f"{done}{left} {tail}%")


def __get_time_difference(
    start_date: datetime.datetime, end_date: datetime.datetime
) -> str:
    hours, minutes = get_time_difference(start_date, end_date)

    hours_string = str(hours).zfill(2)
    minutes_string = str(minutes).zfill(2)

    return f"{hours_string}h {minutes_string}m"


def __get_day(date: datetime.datetime) -> str:
    if (datetime.datetime.now() - date).days > 7:
        fmt = "%Y-%m-%d %H:%M"
    else:
        fmt = "%a, %H:%M"

    return date.strftime(fmt)
