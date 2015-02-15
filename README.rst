bergenholmclient
===============

bergenholmclient is a CLI tool for Bergenholm.

Installation
------------

Run commands below: 

.. code-block:: console

    $ git clone https://github.com/yosshy/bergenholmclient.git
    $ cd bergenholmclient
    $ sudo -E pip install --upgrade .

Test bergenholmclient:

.. code-block:: console

    $ bergenholmclient
    Usage: bergenholmclient [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --debug
      --url URL
      --help     Show this message and exit.
    
    Commands:
      group     group operations
      host      host operations
      template  template operations

Usage
-----

bergenholmclient has 3 subcommands below:

* host
* group
* template

You can see the help message like below:

.. code-block:: console

    $ bergenholmclient host
    Usage: bergenholmclient host [OPTIONS] COMMAND [ARGS]...
    
      host operations
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      create  register parameters of a host
      delete  remove parameters of a host
      list    list uuids of host
      show    show parameters of a host
      update  update parameters of a host

And each subcommand has CRUD subminor commands below:

* list
* show <id>
* create <id> <file>
* update <id> <file>
* delete <id>

You can see the help message like below:

.. code-block:: console

    $ bergenholmclient host show --help
    Usage: bergenholmclient host show [OPTIONS] UUID
    
      show parameters of a host
    
    Options:
      --all   includes parameters from groups
      --help  Show this message and exit.

For example, listing hosts and show parameters of a host are below:

.. code-block:: console

    $ bergenholmclient host list
    564d81fd-37d8-552b-0c40-80b76178aea2
    564ded7e-818b-a8b9-dba6-8f44ece7882b
    default
    register
    
    $ bergenholmclient host show 564ded7e-818b-a8b9-dba6-8f44ece7882b
    {
      "groups": [
        "centos6",
        "centos.amd64"
      ],
      "hostname": "test-200",
      "ipaddr": "192.168.10.200"
    }

"host show" and "group show" has an extra option "--all".
"host show <uuid> --all" shows final parameters merged with group
parameters and replaced Jinja2 variables with other parameters.
"group show <name> --all" show all parameters merged with other
groups specified in "groups" parameter.

Say you will update a host entry. You have to run commands below:

.. code-block:: console

    $ bergenholmclient host show 564ded7e-818b-a8b9-dba6-8f44ece7882b > /tmp/json
    $ nano /tmp/json
    $ bergenholmclient host update 564ded7e-818b-a8b9-dba6-8f44ece7882b /tmp/json
