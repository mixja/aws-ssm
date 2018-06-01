import os
import boto3
import re
from six import string_types

class SSM:
  def __init__(self, names=None, parser=None, delimiter='/', decorator=None):
    self._values = {}
    self._handler = None
    names = names or os.environ.get('SSM_PARAMETERS')
    if names is None:
      return
    if isinstance(names, string_types):
      names = re.split(' |,', names)
    if type(names) is not list:
      raise TypeError("Parameters must be of type list or string but is of type %s" % type(params))
    self._names = names
    self._parser = parser
    self._delimiter = delimiter
    self._client = boto3.client('ssm')
    self.get_parameters(names)
  def __call__(self, *args):
    if callable(args[0]):
      self._handler = args[0]
      return args[0]
    else:
      event = args[0]
      if (event.get('source') == 'aws.ssm' and 
          event.get('detail-type') == 'Parameter Store Change' and
          event.get('detail',{}).get('name') in self._values.keys() and 
          event.get('detail',{}).get('operation') == 'Update'):
        self.get_parameters(names=[event['detail']['name']])
      return self._handler(*args)
  def __getitem__(self, parameter):
    return self._values.get(parameter)
  def get_parameters(self, names=None):
    names = names or self._names
    parameters = self._client.get_parameters(Names=names,WithDecryption=True)
    for parameter in parameters.get('Parameters',[]):
      self._values[parameter['Name']] = parameter['Value']
      if self._parser is None:
        # Split parameter by delimiter removing the first level and converting to environment variable
        # e.g. /my-stack/db/password will return ['db','password'], which will get converted to DB_PASSWORD
        parts = parameter['Name'].strip(self._delimiter).split(self._delimiter)
        if len(parts) > 1:
          key = '_'.join(parts[1:]).upper()
          os.environ[key] = parameter['Value']
        # If the parameter has no "levels" then just use the parameter name as the environment variable as is
        # e.g. if the parameter name is my_stack then the environment variable my_stack will be set
        else:
          os.environ[parts[0]] = parameter['Value']
      else:
        parsed = self._parser(parameter['Value'])
        os.environ[parsed[0]] = parsed[1]