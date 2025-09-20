#  Copyright (c) 2024 seamus@corvideon.ie
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


from invoke import task

SRC_ROOT = "src/promptbouncer/"
TEST_ROOT = "src/test/"


@task
def test(c):
    print("Running unit tests...")
    c.run("python -m unittest discover -v")


@task
def mypy(c):
    print("Running mypy...")
    c.run(f"mypy {SRC_ROOT}")
    c.run(f"mypy {TEST_ROOT}")


@task
def formatter(c):
    print("Running black formatter...")
    c.run(f"python -m black {SRC_ROOT}")
    c.run(f"python -m black {TEST_ROOT}")


@task
def linter(c):
    print("Running flake8...")
    # E501 is turned off - ignore long lines and whitespaces
    c.run(f"flake8 --extend-ignore=E501,W291,W293 {SRC_ROOT}")
    c.run(f"flake8 --extend-ignore=E501,W291,W293 {TEST_ROOT}")


@task
def bandit(c):
    print("Running bandit security checks...")
    c.run(f"bandit -r {SRC_ROOT}")
    c.run(f"bandit -r {TEST_ROOT}")


@task
def isort(c):
    print("Running isort...")
    c.run(f"isort --atomic .")


@task
def checks(c):
    print("Running all checks...")
    isort(c)
    mypy(c)
    formatter(c)
    linter(c)
    bandit(c)
    test(c)


@task
def api(c):
    print("Running prod FastAPI server for Prompt Bouncer..")
    c.run("cd promptbouncer; uvicorn main:app --port 10001")


@task
def ui(c):
    print("Running streamlit UI Prompt Bouncer..")
    c.run("streamlit run ./src/ui/main.py")

