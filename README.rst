aws-ssm
=======

This package provides an `SSM` class that injects parameters from the AWS EC2 Systems Manager (SSM) parameter store into a dictionary and also values as environment variables.  

If using AWS Lambda, the class can be used as a decorator on your handler function to automatically detect EC2 parameter store events and dynamically update parameter values if a change to a parameter is detected.

Usage
-----

.. code:: python
  
  from aws_ssm import SSM

  # The names parameter is required and is typically supplied as a list of parameter names 
  # The names parameter can also be a space/comma-delimited string, which is useful if injecting names via environment variables
  ssm = SSM(names='/myapp/db/password,/myapp/db/name')

  # After creating the SSM object, the parameter values are available as dictionary keys
  db_password = ssm['/myapp/db/password']

  # By default SSM will also create environment variables based upon removing the top level of the parameter name
  # E.g. for '/myapp/db/password' an environment variable of 'DB_PASSWORD' will be created
  db_password = os.environ['DB_PASSWORD']

  # For environment variable injection, the default delimiter is '/' but can be overriden via the delimiter parameter
  ssm = SSM(names=['/my-app.db.password'], delimiter='.')

  # If you encode the environment variable key in the value you can define a parser lambda function
  # E.g. assuming the value of /my-app/db/password is 'MYSQL_DB_PASSWORD=abc123'
  ssm = SSM(names=['/my-app/db/password'], parser=lambda x: x.split('='))
  print(os.environ['MYSQL_DB_PASSWORD']) # outputs abc123

  # For Lambda functions you can decorate your handlers with the manager object
  # This will detect SSM parameter store CloudWatch events and dynamically update parameter values
  # if a parameter currently managed by the manager is updated
  #
  # Note this requires you to configure the ssm object as your Lambda function handler for your application
  # You also need to setup a CloudWatch event to forward SSM parameter store events to this handler
  # E.g. my_function.ssm should be configured as the handler, assuming your function is called my_function and ssm is an instance of the SSM class
  @ssm
  def handler(event, context)
    ...
    ...

Installation
------------

    pip install aws-ssm

Requirements
------------

- boto3_

.. _boto3: https://github.com/boto/boto3

Authors
-------

- `Justin Menga`_

.. _Justin Menga: https://github.com/mixja
