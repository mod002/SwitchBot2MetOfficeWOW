<h1 align="center">SwitchBot ⟼ MetOffice WOW</h1>

Trivial data connector from [SwitchBot](https://www.switch-bot.com/) appliance taking environmental measurements to [Meteorological Office's Weather Observations Website (WOW)](https://wow.metoffice.gov.uk/), making use of [SwitchBot APIs](https://github.com/OpenWonderLabs/SwitchBotAPI).

## Quick Start

Ensure you have [UV](https://github.com/astral-sh/uv) installed.  This is a tool that streamlines dependency management in Python.

### Run the CLI

```commandline
$ uv run upload
```

### Run CI/CD Components

We use [Just](https://github.com/casey/just) to streamline the CI/CD pipeline.

```commandline
$ just fmt

$ just audit
```
