from Fixture.application import Application
import pytest
import json
import os.path
import importlib
import jsonpickle

fixture = None
target = None

@pytest.fixture
def app(request):
   global fixture
   global target
   browser = request.config.getoption("--browser")
   if target is None:
      config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), (request.config.getoption("--target")))
      with open(config_file) as f:
         target = json.load(f)
   if fixture is None or not fixture.is_valid():
      fixture = Application(browser=browser, base_Url=target['baseUrl'])
   fixture.session.ensure_Login(username=target['username'], password=target['password'])
   return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
   def fin():
      fixture.session.ensure_Logout()
      fixture.destroy()
   request.addfinalizer(fin)
   return fixture


def pytest_addoption(parser):
   parser.addoption("--browser", action="store", default="firefox")
   parser.addoption("--target", action="store", default="target.json")



def pytest_generate_tests(metafunc):
   for fixture in metafunc.fixturenames:
      if fixture.startswith("data_"):
         Testdata = load_from_module(fixture[5:])
         metafunc.parametrize(fixture, Testdata, ids=[str(x) for x in Testdata])
      elif fixture.startswith("json_"):
         Testdata = load_from_json(fixture[5:])
         metafunc.parametrize(fixture, Testdata, ids=[str(x) for x in Testdata])

def load_from_module(module):
   return importlib.import_module("data.%s" % module).Testdata


def load_from_json(file):
   with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
      return jsonpickle.decode(f.read())

