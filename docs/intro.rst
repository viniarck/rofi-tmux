Introduction
============

.. image:: images/rft.png

Quickly switches tmux sessions, windows and tmuxinator projects on `rofi <https://github.com/DaveDavenport/rofi>`_. Integrates with `i3wm <http://www.i3wm.org>`_ for a smoother switching workflow, if you have multiple workspaces.

Use Case
--------

I developed rft (rofi-tmux) to optimize my context-switching workflow. As a user who rely completely on tmux for anything shell related, I wanted to have a fuzzy finder switcher, to locate any tmux session or window with seamless integration with i3wm. I guess I've got spoiled by fuzzy finders. Watch the screencast in the Usage section and you'll see what I mean :)

Features
--------

- Switch or kill any tmux session.
- Switch or kill any tmux window, either globally or within the current session.
- Switch to any tmuxinator project.
- Cache last tmux session and window for fast switching back and forth, decreases the number of keystrokes.
- Integration with i3wm for switching to the right workspace seamlessly.
- Extensible for other window managers.
