import json
import ansible.constants as C
from ansible.galaxy.collection import find_existing_collections
from ansible.galaxy.collection.concrete_artifact_manager import ConcreteArtifactsManager
from ansible.cli.config import get_constants
from ansible.plugins.loader import init_plugin_loader
from ..common import load_yml
from ..external.introspect import process, sanitize_requirements

COLLECTIONS = None
COLLECTION_PATHS = C.config.get_config_value('COLLECTIONS_PATHS', variables=get_constants())

class DependencyResolver():
  concrete_artifact_cm = ConcreteArtifactsManager(C.DEFAULT_LOCAL_TMP, validate_certs=False)
  missing_collections = []
  required_collections = []
  dependencies = None

  def __init__(self):
    init_plugin_loader()
    self.collection_paths = C.config.get_config_value('COLLECTIONS_PATHS', variables=get_constants())
    self.available_collections = {}
    for coll in find_existing_collections(COLLECTION_PATHS, self.concrete_artifact_cm, dedupe=False):
      self.available_collections[coll.fqcn] = coll.src.decode('utf-8')

  def resolve(self, collections):
    self.get_coll_paths(collections)
    self.dependencies = process(self.required_collections)
    self.dependencies['python'] = sanitize_requirements(self.dependencies['python'])

  def get_coll_paths(self, collections) -> str:
    for coll in collections:
      name = self.__get_coll_name(coll)
      path = self.available_collections.get(name, None)
      if path:
        self.required_collections.append(path)
      else:
        self.missing_collections.append(name)

  def __get_coll_name(self, collection) -> str:
    if type(collection) == dict:
      return collection.get('name')
    return collection
  
def pip_dry_run(requirements: list[str]):
  from pip._internal.cli.main_parser import parse_command
  from pip._internal.commands import create_command

  cli_args = ['install','--dry-run']
  cli_args.extend(requirements)
  cmd_name, cmd_args = parse_command(cli_args)
  command = create_command(cmd_name, isolated=False)
  options, args = command.parse_args(cli_args)
  try:
    command.main(args)
    command.run(options, args)
  except AssertionError:
    pass # Ignore context related error using CLI from code

def desc_deps(definition_path: str, config: dict):
  resolver = DependencyResolver()
  definition = load_yml(definition_path)
  resolver.resolve(definition['collections'])
  print("Dependencies Identified")
  print("-----------------------")
  print(json.dumps(resolver.dependencies, indent=2))

  py_deps = resolver.dependencies.get('python',[])
  if len(py_deps):
    reqs = map(lambda line: line.lstrip().split(' ')[0], py_deps)
    print("\nBeginning pip *dry-run*\t(Nothing will be installed)")
    print("-----------------------")
    pip_dry_run(reqs)