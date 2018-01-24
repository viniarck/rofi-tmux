Configuration
=============

The only configuration option available is for specifing if you want context-switching integration with any of the supported window managers below. With this integration, as soon as you switch context, rofi-tmux will switch to the appropriate workspace where tmux is running. First, you have to create the json configuration file ``~/.rft`` and then specify which window manager you're running:

.. note::

    If you want to change the algorithm rofi uses, you should change it on rofi rc configuration file itself, "~/.config/rofi/config", for example to uses the fuzzy macher you should set rofi.matching attribute as "fuzzy".

i3wm
----

.. code:: json

    {
        "wm": "i3"
    }

.. note::

    Feel free to send pull requests for other window managers that support multiple workspaces.

