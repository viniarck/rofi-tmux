Usage
=====

Two things you have to keep in mind when using rft:

1. rft doesn't launch a terminal automatically for you, so, if you don't have a tmux session attached yet you're supposed to run rft in the terminal (``rft ss`` or ``rft lp``).
2. rft caches the last tmux session/window you have switched from, so it automatically pre-selects it in the rofi prompt, except if you are in a different workspace, where rft assumes that you probably want to switch over to the same session/window you were before/that is currently opened.


I recommend that you have shortcuts with control modifiers for rft, so if you always have a tmux session running, it's going to be really fast to find this session and switch to it. For example, I use these key bindings on i3wm for launching rft:

.. code:: shell

    bindsym $mod+y exec "$HOME/.local/bin/rft lp"
    bindsym $mod+e exec "$HOME/.local/bin/rft ss"
    bindsym $mod+w exec "$HOME/.local/bin/rft sw"
    bindsym $mod+Shift+d exec "$HOME/.local/bin/rft ks"
    bindsym $mod+Shift+w exec "$HOME/.local/bin/rft kw"
    bindsym $mod4+g exec "$HOME/.local/bin/rft sw --global_scope false"

.. note::

    If you have pip3 installed with the --user flag the executable will be in ~/$HOME/.local/bin/rft.

The first three are the ones that I use the most. They're for loading a tmuxinator project (`lp`), switching to a session (`ss`) and switching to a window globally (`sw`).
So, I set some keys that are near my home row. If you want to check all rft actions available:

.. code:: shell

  ❯ rft
  Usage: rft [OPTIONS] COMMAND [ARGS]...

    RFT (rofi-tmux) switcher.

  Options:
    --debug BOOLEAN  Enables logging at debug level.
    --help           Show this message and exit.

  Commands:
    ks  Kill tmux session.
    kw  Kill tmux window.
    lp  Load tmuxinator project.
    ss  Switch tmux session.
    sw  Switch tmux window.
    v   Print version.

Screencast
----------

Watch this screencast to see rft in action:

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="//www.youtube.com/embed/o6tBNFJW28c" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>
