#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .window_manager import WindowManager
import i3ipc
import logging


class i3WM(WindowManager):
    """Abstraction to handle i3wm"""

    def __init__(self) -> None:
        """Constructor

        """
        self._i3 = i3ipc.Connection()
        self._cur_wks = self._get_cur_workspace()
        self.logger = logging.getLogger(__name__)
        super(i3WM, self).__init__()

    def switch_tmux_workspace(self, session_name) -> None:
        """Switches to the workspace where tmux session_name is running

        :session_name: tmux session name str

        """
        self.logger.debug('cur_i3_wks:{}'.format(self._cur_wks))
        self.logger.debug('i3 switching to workspace: {}'.format(session_name))
        wkps = self._find_tmux_workspace(session_name)
        if wkps:
            wkps.command('workspace {}'.format(wkps.name))

    def is_tmux_not_in_cur_workspace(self, session_name) -> i3ipc.Con:
        """Verifies if tmux is not in the current i3 workspace

        :session_name: tmux sesion name to verify

        """
        workspace = self._find_tmux_workspace(session_name)
        if workspace:
            if not workspace.name == self._cur_wks:
                return workspace
        return False

    def _get_cur_workspace(self) -> str:
        """Finds current workspace

        """
        workspaces = self._i3.get_workspaces()
        for workspace in workspaces:
            if workspace.get('visible'):
                return workspace.get('name')

    def _find_tmux_workspace(self, session_name) -> i3ipc.Con:
        """Finds which workspace tmux is running

        :session_name: tmux sesion name to find

        """
        tree = self._i3.get_tree()
        descendents = tree.descendents()
        workspaces = [
            descendent for descendent in descendents
            if descendent.type == 'workspace'
        ]
        self.logger.debug('finding i3 tmux session {}'.format(session_name))
        for w in workspaces:
            cons = w.find_named(session_name)
            if cons:
                self.logger.debug('tmux session {} is in workspace {}'.format(
                    session_name, w.name))
                return w
