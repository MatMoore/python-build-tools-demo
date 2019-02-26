# Python build tools demo

[This is just a rough outline at the moment]

## What this demo will cover

Going to focus on 3 types of tools

- Installing pythons onto computers
- Managing application dependencies
- (If there's time) creating reusable python packages

Lots of tools have "env" in their name! Don't confuse them!

## Installing pythons

### What gets installed by default (on a mac)

- Usually your OS comes with *some version* of python
- Task: Look at what is installed on your path. What version is it? Are there multiple pythons (python2 and python3)?
- Debugging path issues
- Forcing a particular interpreter `python3 -m pip` - `-m` runs a module
- What is PYTHONPATH and site-packages

### History of python 2 and 3 split
- http://py3readiness.org/
- [Six](https://pypi.org/project/six/)
- Who's still using python 2 on their projects?

### Virtualenv = a copy of your interpreter and packages
- Create one and look inside
- Activate and deactivate
- Check you are isolated from system packages

### Pyenv
- Install lots of pythons side by side

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
- Compatable with semantic versioning ("I want to be on the latest patch version for 2.4")
- Analogous to `Gemfile` and `Gemfile.lock` in ruby
- When you create a project you can choose the python version
- Some workflow improvements - don't need to manage a virtualenv yourself, just use `pipenv run` and `pipenv shell`

### Some alternatives to Pipenv you might come accross
- Poetry
- Multiple `requirements.txt` files
- `mkvirtualenv` for easier virtualenv management

## Creating packages
- Levels of abstraction: classes/functions/data -> modules -> packages -> PyPI package
- Why create standalone packages?
- Look at a setup.py for a real package
- Minimum viable package
- Declaring dependencies
- `setuptools` replaces `distutils`
- Eggs and Wheels
- Typically you want to test against multiple versions of python using CI
- Publishing to pypi
- https://keepachangelog.com/en/1.0.0/

## Other resources
- [Hitchhikers guide to python](https://docs.python-guide.org/)
- [Interpreter options](https://docs.python.org/3/using/cmdline.html#interface-options)
- [Installing packages with pip and virtualenv](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)
- [Distributing packages](https://docs.python.org/3/distributing/index.html)
