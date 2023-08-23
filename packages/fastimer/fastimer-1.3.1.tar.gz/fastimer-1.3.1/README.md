# ⏱️ ⏰ 🕰️ Fastimer

[![PyPi](https://img.shields.io/pypi/v/fastimer)](https://pypi.org/project/fastimer/) [![pylint](https://github.com/vkostyanetsky/Fastimer/actions/workflows/pylint.yml/badge.svg)](https://github.com/vkostyanetsky/Fastimer/actions/workflows/pylint.yml) [![black](https://github.com/vkostyanetsky/Fastimer/actions/workflows/black.yml/badge.svg)](https://github.com/vkostyanetsky/Fastimer/actions/workflows/black.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

It is a simple CLI timer to track fasts, designed specifically to help you monitor your fasting intervals.  

## 😮 Why did you make this?

Yeah, there are plenty of apps like this one, you are right. I wrote this one simply out of annoyance when the [Zero](https://www.zerolongevity.com/) app for Android once again refused to show me a fast I did. I was tapping on the calendar inside the application, but it was doing nothing.

I have no idea what was wrong with it. Anyway, the task is not that hard, so I just wrote my own timer ¯\\\_(ツ)\_/¯

## 🙃 How to install it?

I have nothing to surprise you here:

```commandline
pip install fastimer
```

## 🙂 How to use it?

It is a console application. So you can run this:

```commandline
fastimer --help
```

The script will show you the available commands. 

By default, Fastimer expects to see your data in the user's home directory (`%USERPROFILE%\Fastimer` on Windows, for example). Of course, you can store it anywhere else using a directory junction or `--path` option.

To be short, you want a fasting timer to do four things.

### 1. To start a new fast

The first thing is creating a new fast. Usage:

```commandline
fastimer start 20
```

Twenty above is the number of hours you are going to spend fasting. You can omit this option (the default is 16).

### 2. To see how fasting is going

Once you have started a fast, it is convenient to use `fastimer show last` command. It shows elapsed time, remaining time, and something that looks like a progress bar to visualize your spilled blood, sweat, and tears :)

Here is an example:

```
ACTIVE FAST

From: Tue, 11:25
Goal: Wed, 07:25 (20 hours)

Fasting zones:

1. Anabolic:    from Tue, 11:25
2. Catabolic:   from Tue, 15:25 <-- you are here
3. Fat burning: from Wed, 03:25
4. Ketosis:     from Wed, 11:25
5. Anabolic:    from Fri, 11:25

######################------------------ 56.5%

Elapsed time:   11h 17m
Remaining:      08h 43m
```

Please note that the `fastimer show last` command is the default one. So you can simply type `fastimer show` or `fastimer`: both of them have the same meaning.

In addition, you can use `fastimer show prev` command to show a fast before the last one. 

### 3. To stop or cancel the fast you've started

When the fast is active, the `fastimer stop` command allows you to stop your fast when you decide to do so. It means that the fast is over and you wish to store the fast in the app's history.

Usage:

```commandline
fastimer stop
```

Another option is to cancel the fast. It means you wish to delete the information about this fast by for some weird reason.

Usage:

```commandline
fastimer cancel
```

### 4. To see how well you're doing

```commandline
fastimer info
```

This command shows you statistical data and earned [achievements](ACHIEVEMENTS.md).

For instance:

```
FASTING STATISTICS

Completed Fasts:         33 out of 34
Total Fasting Time:      437h 26m
Average Fast Length:     13h 15m
Longest Fast Length:     18h 12m
Longest Fasting Streak:  20 days
Current Fasting Streak:  3 days

Achievements:
- COPPER WALKER (level 2 badge out of 9). Twenty five fasts completed!
- COPPER MAN OF HABIT (level 2 badge out of 9). Ten completed fasts in a row!
```

## 🤔 Questions 

### Where can I see or edit my fasts?

The script stores all fasts in `fasts.yaml` file in the working directory. It has the [YAML](https://en.wikipedia.org/wiki/YAML) format, which is quite human-readable, so you can just open it in your lovely text editor.

For instance, the completed fast in the journal looks like this:

```yaml
- length: 16
  started: 2022-07-20 19:59:14
  stopped: 2022-07-21 12:00:33
```

The first parameter is the length of the fast, the second is the start date, and the third is the completion date.

For an ongoing fast, the third parameter is omitted.