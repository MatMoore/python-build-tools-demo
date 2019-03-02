# Python build tools demo
This demo will show how we can manage python source code, as of early 2019, and how to avoid this:

<img alt="XKCD 1987: Python environment" src="https://raw.githubusercontent.com/MatMoore/python-build-tools-demo/master/python_environment_2x.png" width="492" height="487"/>

## What we'll cover

The demo will be split into 3 tasks:

- Installing pythons onto computers
- Managing application dependencies
- (If there's time) creating reusable python packages

### Opinions ahoy
> "There should be one-- and preferably only one --obvious way to do it." - The Zen of Python

Sadly, this is not the case in Python for the tasks I listed above. In this demo I will introduce the core tools that the python ecosystem depends on (pip and virtualenv/venv), and their limitations.

Where there are multiple ways to do something I will just discuss one solution I'm familiar with, but I'll list alternatives you can research if you want to try something else.

## Installing pythons

### What gets installed by default?

- Usually your OS comes with *some version* of python
- Task: Look at what is installed on your path. What version is it? Are there multiple pythons (python2 and python3)?
- Debugging path issues
- `pip` is the python package manager, and should also be on your path. It's installed as part of the python installation.
- What is PYTHONPATH and site-packages?
- You can also run pip by passing an option to the python interpreter: `python3 -m pip`. The `-m` can be used to execute the code in any python module.

### Isolating python projects from each other
#### Virtualenv = a copy of your interpreter and packages
Normally when you install stuff through the `pip` command, you are installing it to some site-packages directory somewhere.

If you have a lot of different projects, they will all share the same dependencies, and your development environment will be different to production.

We use virtualenvs to solve this problem. A virtualenv is a project-specific directory that dependencies can be installed to, so you can isolate the dependencies from different projects and manage them separately.

It contains its own copy of the python interpreter used to create it, and its own copy of pip.

#### Creating virtualenvs
There are two tools to create virtualenvs:
- virtualenv is the original tool, and needs to be itself installed through pip
- on newer versions of python you can just run `python -m venv DIRECTORY` to create one

Virtualenvs shouldn't be checked into github, because they can contain code that is compiled for a particular platform. Instead you should create the virtualenv when you check out a project to work on (or use a tool that does this for you).

#### Workflow for using virtualenvs directly
After creating a virtualenv, running `source bin/activate` will "activate" it. This changes your path variables so that `python` and `pip` point to the ones inside your virtualenv. You should see the name of the virtualenv added to your shell prompt. 

When you're done working inside the virtualenv, run `deactivate` to go back to your normal shell.

*NOTE: You can also directly run python or pip by using the full path to your virtualenv, for example `my-env/bin/python my_script.py` or `my-env/bin/pip install foo`.*

#### Try it out
- Create one and look inside
- Activate and deactivate
- Check you are isolated from system packages
- Check what happened to `sys.path`

### History of python 2 and 3 split
- http://py3readiness.org/
- [Six](https://pypi.org/project/six/)
- Who's still using python 2 on their projects?

### Using up to date versions of python
- [Check the documentation](https://www.python.org/doc/versions/) for details of each version
- New versions are released all the time (8 bug fix releases in 2018)
- You can see what features are upcoming via the [Python Enhancement Propsals (PEPs)](https://www.python.org/dev/peps/)

#### Installing multiple versions side by side
- **Pyenv** is a tool that lets you install lots of pythons side by side
- If using different pythons for different projects, you don't break everything when you upgrade your system

#### Try it out
You can install pyenv using homebrew (MacOS) or [through an installer](https://github.com/pyenv/pyenv-installer).

Once you’ve installed it, you can run `pyenv install -l` to list all the versions of python. Ignore all the ones with prefixes and suffixes and just install the latest one. For example
`pyenv install 3.6.5`

Run `python` and you should see something like this:

```
Python 3.6.5 (default, Feb  9 2019, 17:16:17)
[GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.10.44.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Boom! Now you have that version of python. To set it as the default for your project run `pyenv local 3.6.5`. It will create a file called `.python-version` so that pyenv will always use that python version. It will also make sure the `pip` command is the one for that python version.

## Managing application dependencies

### requirements.txt files
- `requirements.txt` specifies minimum, maximum or exact versions of your dependencies
- Note that it's an *incomplete* specification if it doesn't contain transitive dependencies or exact versions
- `pip freeze` can generate a complete `requirements.txt` from your local environment

### Problems with pip and requirements.txt
Multiple invocations of pip install can return different results, for various reasons:

- New versions of packages may have been released, so the second invocation gets newer stuff
- You place a lot of trust in the repository to not [change or remove packages that existed previously](https://www.theregister.co.uk/2016/03/23/npm_left_pad_chaos/)

It's hard to debug stuff if different environments run different code.

Upgrading stuff is usually a good thing, but we should be in control of when that happens, so we can manage it like any other code change.

If dependencies follow [semantic versioning](https://semver.org/), then:

- Patch upgrades are bug fixes or security patches, which are always desirable
- Minor upgrades are intended to be backwards compatable (but might not be)
- Major upgrades are not backwards compatable and may require effort to upgrade

If you freeze all your dependencies, then your build will be repeatable but you'll probably be stuck with those versions for a long time. Pip doesn't make it very easy to safely upgrade packages.

Pip is also [notoriously bad at resolving overlapping requirements](https://github.com/pypa/pip/issues/988), which can lead to [all sorts of strange errors](https://medium.com/knerd/the-nine-circles-of-python-dependency-hell-481d53e3e025).

### Enter Pipenv and Pipfile
- `Pipfile` replaces `requirements.txt` and may become the standard format in the future
- "Locking" with `Pipenv.lock` ensures repeatable builds
- Pipfile is for the direct dependencies you care about
- [Compatable with semantic versioning](https://pipenv.readthedocs.io/en/latest/basics/#specifying-versions-of-a-package) ("I want to be on the latest patch version for 2.4")
- Analogous to `Gemfile` and `Gemfile.lock` in ruby
- When you create a project you can choose the python version to use
- `pyenv` and `pipenv` can be used together

#### Try it out
Install it by running: `pip install pipenv`
Then run `pipenv install` with no arguments to set up your project.

Pipenv builds on top of pip and virtualenv so the workflow is a bit simpler.

In pipenv-land, you can substitute `pip install` for `pipenv install`, and you don’t need to use virtualenv at all (pipenv creates it for you).

You just need one command - `pipenv` - to add, remove, or upgrade dependencies. It also makes builds deterministic by capturing the exact versions of everything in your dependency tree in the `Pipfile.lock` file. This doesn’t matter much when you’re setting up the project, but will save you a lot of pain later down the line.

### Some alternatives to Pipenv you might come accross
#### Different tools
[Poetry](https://github.com/sdispater/poetry) solves many of the same problems as Pipenv. [Hatch](https://github.com/ofek/hatch) also has some overlap. I haven't tried either of these tools myself, but they seem a bit more geared towards distributing packages, whereas Pipenv + pipfile is [deliberately not designed for this](https://pipenv.readthedocs.io/en/latest/advanced/#pipfile-vs-setuppy).

[Tox](https://tox.readthedocs.io) is a popular way to test against multiple versions of python. Again, more geared towards libraries than applications.

To give an idea of the relative adoption, I plotted the [PyPi download stats](https://packaging.python.org/guides/analyzing-pypi-package-downloads/) for the last few months:
![Popularity of tools over the last few months](https://raw.githubusercontent.com/MatMoore/python-build-tools-demo/master/tool-usage.png)

#### Sticking with requirements.txt
You can also just use pip + virtualenv on their own. In this case you’ll need to create a `requirements.txt` file with all your dependencies in.

With this workflow, you add all the dependencies to `requirements.txt` and then run
`pip install -r requirements.txt` whenever that file is changed.

You will need to explicitly [pin your packages](https://nvie.com/posts/pin-your-packages/) to get repeatable builds. However, in order to upgrade a dependency, you then need to re-resolve **its** dependencies, which you can’t do if they’re all pinned. IMO, this approach makes it harder to maintain larger projects.

## Creating reusable packages
- Levels of abstraction: classes/functions/data -> modules -> packages -> PyPI package
- Why create standalone packages?
- Look at [a setup.py for a real package](https://github.com/stub42/pytz/blob/master/src/setup.py)
- Create a [minimum viable package](https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use)
- Declaring dependencies
- `setuptools` replaces `distutils`
- Eggs -> Wheels
- `setup.py develop` (quite useful when packaging command line scripts)
- Typically you want to test against multiple versions of python using CI
- Publishing to pypi
- https://keepachangelog.com/en/1.0.0/

## Other resources
- [Python's new package landscape](http://andrewsforge.com/article/python-new-package-landscape/) - blog post covering the same content as this demo
- [Hitchhikers guide to python](https://docs.python-guide.org/) - an opinionated guide on how to set up python projects
- [Interpreter options](https://docs.python.org/3/using/cmdline.html#interface-options) - official documentation
- [Installing packages with pip and virtualenv](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) - official documention
- [Distributing packages](https://docs.python.org/3/distributing/index.html) - official documentation
