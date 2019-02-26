# Python build tools demo

[This is just a rough outline at the moment]

<img alt="XKCD 1987: Python environment" src="https://raw.githubusercontent.com/MatMoore/python-build-tools-demo/master/python_environment_2x.png" width="492" height="487"/>

## What this demo will cover

Going to focus on 3 types of tools

- Installing pythons onto computers
- Managing application dependencies
- (If there's time) creating reusable python packages

*Note: Lots of tools have "env" in their name! Don't get them confused!*

## Installing pythons

### What gets installed by default?

- Usually your OS comes with *some version* of python
- Task: Look at what is installed on your path. What version is it? Are there multiple pythons (python2 and python3)?
- Debugging path issues
- `pip` is the python package manager, and should also be on your path. It's installed as part of the python installation.
- What is PYTHONPATH and site-packages?
- You can also run pip by passing an option to the python interpreter: `python3 -m pip`. The `-m` can be used to execute the code in any python module.


### History of python 2 and 3 split
- http://py3readiness.org/
- [Six](https://pypi.org/project/six/)
- Who's still using python 2 on their projects?

### Virtualenv = a copy of your interpreter and packages
Normally when you install stuff through the `pip` command, you are installing it to some site-packages directory somewhere.

If you have a lot of different projects, they will all share the same dependencies, and your development environment will be different to production.

We use virtualenvs to solve this problem. A virtualenv is a project-specific directory that dependencies can be installed to, so you can isolate the dependencies from different projects and manage them separately.

It contains its own copy of the python interpreter used to create it, and its own copy of pip.

There are two tools to create virtualenvs:
- virtualenv is the original tool, and needs to be itself installed through pip
- on newer versions of python you can just run `python -m venv DIRECTORY` to create one

Virtualenvs shouldn't be checked into github, because they can contain code that is compiled for a particular platform. Instead you should create the virtualenv when you check out a project to work on (or use a tool that does this for you).

After creating a virtualenv, running `source bin/activate` will "activate" it. This changes your path variables so that `python` and `pip` point to the ones inside your virtualenv. You should see the name of the virtualenv added to your shell prompt. 

When you're done working inside the virtualenv, run `deactivate` to go back to your normal shell.

#### Try it out
- Create one and look inside
- Activate and deactivate
- Check you are isolated from system packages

### Pyenv
- Install lots of pythons side by side
- If using different pythons for different projects, you don't break everything when you upgrade your system

#### Try it out
You can install pyenv using homebrew (Mac OS) or [through an installer](https://github.com/pyenv/pyenv-installer).

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

- `requirements.txt`
- Semantic versioning
- `pip freeze`
- Problems with transitive dependencies

### Pipenv and Pipfile
- Quite new
- `Pipfile` replaces `requirements.txt` and is likely to become the standard format
- Locking ensures repeatable builds
- Pipfile is for direct dependencies
- [Compatable with semantic versioning](https://pipenv.readthedocs.io/en/latest/basics/#specifying-versions-of-a-package) ("I want to be on the latest patch version for 2.4")
- Analogous to `Gemfile` and `Gemfile.lock` in ruby
- When you create a project you can choose the python version

#### Try it out
Install it by running: `pip install pipenv`
Then run `pipenv install` with no arguments to set up your project.

Pipenv builds on top of pip and virtualenv so the workflow is a bit simpler.

In pipenv-land, you can substitute `pip install` for `pipenv install`, and you don’t need to use virtualenv at all (pipenv creates it for you).

You just need one command - `pipenv` - to add, remove, or upgrade dependencies. It also makes builds deterministic by capturing the exact versions of everything in your dependency tree in the `Pipfile.lock` file. This doesn’t matter much when you’re setting up the project, but will save you a lot of pain later down the line.

### Some alternatives to Pipenv you might come accross
[Poetry](https://github.com/sdispater/poetry) is a competitor to pipenv and seems very similar. I haven’t actually tried it yet, but it probably works just as well.

I plotted the [PyPi download stats](https://packaging.python.org/guides/analyzing-pypi-package-downloads/) to show the relative adoption of some different tools:
![Popularity of tools over the last few months](https://raw.githubusercontent.com/MatMoore/python-build-tools-demo/master/tool-usage.png)

You can also just use pip + virtualenv on their own. In this case you’ll need to create a file called `requirements.txt` file with all your dependencies in. However, this can become hard to manage for larger projects.

With this workflow, you add all the dependencies to `requirements.txt` and then run
`pip install -r requirements.txt` whenever that file is changed. You will need to explicitly [pin your packages](https://nvie.com/posts/pin-your-packages/) to get repeatable builds. However, in order to upgrade a dependency, you then need to re-resolve **its** dependencies, which you can’t do if they’re all pinned!

Note that pipenv + pipfile is not designed for libraries: https://pipenv.readthedocs.io/en/latest/advanced/#pipfile-vs-setuppy

## Creating packages
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
- [Hitchhikers guide to python](https://docs.python-guide.org/)
- [Interpreter options](https://docs.python.org/3/using/cmdline.html#interface-options)
- [Installing packages with pip and virtualenv](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)
- [Distributing packages](https://docs.python.org/3/distributing/index.html)
