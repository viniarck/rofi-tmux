Configuration
=============

All configuration is optional, and is to be written in a json file at ``~/.rft``.

- ``wm``

  Defines which window manager we want to integrate with for smoother context-switching.
  With this integration, as soon as you switch context, rofi-tmux will
  automatically focus window where tmux is running.
  Currently the only supported window manager is ``i3``, which is the default value.
  
  .. note::
  
      Feel free to send pull requests for other window managers that support multiple workspaces.

- ``tmux_title_rgx``

  Only applicable when ``wm`` config is set.
  This is the regular expression used by window-manager integration logic to locate the
  window housing specific tmux session. Generally you'd like this (roughly) to match
  your tmux configuration. The pattern also supports two optional
  placeholders that will be automatically expanded:
 
  + ``{session}`` will be expanded into tmux session name
  + ``{window}`` will be expanded into tmux window name

  Eg if you have ``set -g set-titles-string "#S / #W / #T"`` in your .tmux.conf, you
  might want to set to this value:

  .. code:: json
  
      {
          "tmux_title_rgx": "^{session} / {window} / "
      }


- ``ignored_sessions``

  Optional list of tmux session names that should be ignored when building the
  selection menu.
  Eg:

  .. code:: json
  
      {
          "ignored_sessions": ["session-name", "other-session-name"]
      }


.. note::

    If you want to change the algorithm rofi uses, you should change it on rofi rc configuration file itself, "~/.config/rofi/config", for example to uses the fuzzy macher you should set rofi.matching attribute as "fuzzy".

config example using i3wm
-------------------------

.. code:: json

    {
        "wm": "i3",
        "tmux_title_rgx": "^tmux-{session}-{window}",
        "ignored_sessions": ["session-name-to-ignore"]
    }

