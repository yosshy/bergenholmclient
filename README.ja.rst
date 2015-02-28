bergenholmclient
================

bergenholmclient は Bergenholm 用のコマンドラインツールです。

インストール
------------

下記のコマンドを実行します。

.. code-block:: console

    $ git clone https://github.com/yosshy/bergenholmclient.git
    $ cd bergenholmclient
    $ sudo -E pip install --upgrade .

bergenholmclient をテストします。

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

使用法
------

bergenholmclient は以下のサブコマンドがあります。

* host
* group
* template
* power

下記のようにするとヘルプメッセージが表示されます。

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

host, group, template サブコマンドには作成・削除・更新・表示の子コマン
ドがあります。

* list
* show <id>
* create <id> <file>
* update <id> <file>
* delete <id>

power サブコマンドには電源状態表示／変更の子コマンドがあります。

* status <id>
* on <id>
* off <id>
* reset <id>

下記のようにするとヘルプメッセージが表示されます。

.. code-block:: console

    $ bergenholmclient host show --help
    Usage: bergenholmclient host show [OPTIONS] UUID
    
      show parameters of a host
    
    Options:
      --all   includes parameters from groups
      --help  Show this message and exit.

例として、ホスト一覧表示と１ホストのパラメータ表示を実行してみましょう。

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

host show と group show には --all オプションがあります。
host show <uuid> --all は、グループパラメータを継承し、Jinja2 変数を他
のパラメータで置換したホストパラメータを表示します。
group show <name> --all は、他のグループパラメータを継承したグループパ
ラメータを表示します。

ホストの登録を更新するとします。以下のコマンドを実行して下さい。

.. code-block:: console

    $ bergenholmclient host show 564ded7e-818b-a8b9-dba6-8f44ece7882b > /tmp/json
    $ nano /tmp/json
    $ bergenholmclient host update 564ded7e-818b-a8b9-dba6-8f44ece7882b /tmp/json
