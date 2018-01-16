#!/usr/bin/env python
# -*- coding: utf-8 -*-

import i3ipc
import libtmux
import logging
import json
import io
import os
import rofi
import shutil
import subprocess
import sys
logging.basicConfig(filename='/tmp/.tmux_rofi.log', level=logging.DEBUG)


class RofiTmux(object):
    """Abstraction to interface with rofi tmux, tmuxinator and i3"""

    def __init__(self, debug=False):
        """Constructor"""
        self._rofi = rofi.Rofi()
        self._libts = libtmux.Server()
        self._sessions = None
        self._has_i3 = shutil.which('i3')
        if self._has_i3:
            self._i3 = i3ipc.Connection()
        self._cur_tmux_s = None
        self._cur_i3_s = None
        self.logger = logging.getLogger(__name__)
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self._cache_f = os.path.join(os.environ.get('HOME'), '.rofi_tmux')
        self._cache = {}
        self._register_cur_sessions()
        self._load_cache()

    def _load_cache(self) -> None:
        """Loads last tmux sessions and window cache

        """
        try:
            with open(self._cache_f, 'r') as f:
                self._cache = json.load(f)
        except FileNotFoundError as e:
            self._cache = {'_last_tmux_s': None, '_last_tmux_w': None}
        self.logger.debug('loaded cache: {}'.format(self._cache))

    def _write_cache(self) -> None:
        """Writes cache

        """
        try:
            with open(self._cache_f, 'w') as f:
                f.write(
                    json.dumps(
                        self._cache,
                        indent=4,
                        sort_keys=True,
                        separators=(',', ': '),
                        ensure_ascii=False))
            self.logger.debug('wrote cache: {}'.format(self._cache))
        except IOError as e:
            raise e

    def _register_cur_sessions(self) -> None:
        """Registers the current tmux and i3 sessions

        """
        if self._has_i3:
            self._cur_i3_s = self._find_cur_i3_workspace()
            self.logger.debug('_cur_i3_s: {}'.format(self._cur_i3_s))
        try:
            self._sessions = self._libts.list_sessions()
            self.logger.debug('_sessions: {}'.format(self._sessions))
        except libtmux.exc.LibTmuxException as e:
            # if there are no sessions running load_project takes place
            self.load_tmuxinator()
        self._cur_tmux_s = self._get_cur_session()
        self.logger.debug('_cur_tmux_s: {}'.format(self._cur_tmux_s))

    def _find_cur_i3_workspace(self) -> str:
        """Finds current i3 workspace

        """
        workspaces = self._i3.get_workspaces()
        for workspace in workspaces:
            if workspace.get('visible'):
                return workspace.get('name')

    def _get_cur_session(self) -> str:
        """Gets current tmux session name

        """
        out, err = subprocess.Popen(
            """tmux list-panes -F '#{pane_tty} #{session_name}'""",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()
        for line in out.splitlines():
            return line.decode('utf-8').split()[-1]

    def _switch_i3_tmux_workspace(self, session_name) -> bool:
        """Switches to i3 workspace where tmux is running

        :session_name: tmux sesion name to switch to

        """
        tree = self._i3.get_tree()
        descendents = tree.descendents()
        workspaces = [
            descendent for descendent in descendents
            if descendent.type == 'workspace'
        ]
        for w in workspaces:
            cons = w.find_named(session_name)
            if cons:
                # only switches if current workspace is different
                if not w.name == self._cur_i3_s:
                    self.logger.debug('_cur_i3_s:{}'.format(self._cur_i3_s))
                    self.logger.debug('switching i3 to workspace: {}'.format(
                        w.name))
                    w.command('workspace {}'.format(w.name))
                    return True

    def _get_tmuxinator_projects(self) -> list:
        """Gets tmuxinator projects name

        """
        out, err = subprocess.Popen(
            "tmuxinator list",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()
        projects = []
        for line in out.splitlines():
            line_str = line.decode('utf-8')
            if "tmuxinator projects" in line_str:
                continue
            projects += line_str.split()
        return projects

    def _get_session_by_name(self, session_name) -> libtmux.session.Session:
        """Gets libtmux.session.Session

        :session_name: session name

        """
        if self._sessions:
            for s in self._sessions:
                if s.name == session_name:
                    return s

    def _rofi_tmuxinator(self, rofi_msg, rofi_err) -> None:
        """Launches rofi for loading a tmuxinator project
        Updates the number of tmux sessions

        :rofi_msg: rofi displayed message
        :err_msg: rofi error message

        """
        projects = self._get_tmuxinator_projects()
        if projects:
            res, key = self._rofi.select(rofi_msg, projects)
            if key == 0:
                out, err = subprocess.Popen(
                    "tmuxinator {}".format(projects[res]),
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE).communicate()
                # that's when the user didn't have any prior sessions
                if not self._cur_tmux_s:
                    return
                self._sessions = self._libts.list_sessions()
                if self._has_i3:
                    self._switch_i3_tmux_workspace(self._sessions[res].name)
                self._sessions[res].switch_client()
        else:
            self._rofi.error(rofi_err)

    def load_tmuxinator(self) -> None:
        """Loads tmuxinator project

        """
        self._rofi_tmuxinator(
            rofi_msg='Tmuxinator project: ',
            rofi_err='There are no projects available')

    def _rofi_tmux_session(self, action, rofi_msg) -> None:
        """Launches rofi for a specific tmux session action

        :action: 'switch', 'kill'
        :rofi_msg: rofi displayed message

        """
        if self._sessions:
            sessions_list = [s.name for s in self._sessions]
            sel = 0
            last_session = self._cache['_last_tmux_s']
            # if cached then select last session
            if last_session:
                sel = sessions_list.index(last_session)
            else:
                # select current session as a fallback
                sel = sessions_list.index(self._cur_tmux_s)
            res, key = self._rofi.select(rofi_msg, sessions_list, select=sel)
            if key == 0:
                if action == 'switch':
                    if self._has_i3:
                        self._switch_i3_tmux_workspace(
                            self._sessions[res].name)
                    try:
                        self._sessions[res].attach_session()
                    except libtmux.exc.LibTmuxException as e:
                        # there are no attached clients just switch instead.
                        self._sessions[res].switch_client()
                    self._cache['_last_tmux_s'] = self._cur_tmux_s
                    self._write_cache()
                elif action == 'kill':
                    self._sessions[res].kill_session()
                else:
                    self._rofi.error('This action is not implemented')
        else:
            self._rofi.error(rofi_err)

    def switch_session(self) -> None:
        """Switches tmux session

        """
        self._rofi_tmux_session(action='switch', rofi_msg='Switch session: ')

    def kill_session(self) -> None:
        """Kills tmux session

        """
        self._rofi_tmux_session(action='kill', rofi_msg='Kill session: ')

    def _rofi_tmux_window(self, action, session_name, global_scope,
                          rofi_msg) -> None:
        """Launches rofi for a specific tmux window action

        :action: 'switch', 'kill'
        :session_name: if it's not None, the scope is limited to this session
        :global_scope: if True, it will take into account all existent windows
        :rofi_msg: rofi displayed message

        """
        windows = None
        if session_name:
            session = self._get_session_by_name(session_name=session_name)
            windows = session.list_windows()
        else:
            session = self._get_session_by_name(
                session_name=self._get_cur_session())
            if session:
                if global_scope:
                    windows = []
                    for s in self._sessions:
                        windows += s.list_windows()
                else:
                    windows = session.list_windows()

        if windows:
            # if cached then select last session
            sel = 0
            last_window = self._cache['_last_tmux_w']
            if last_window:
                sel = sessions_list.index(last_window)
            # TODO: also find the last workspace, check substr
            # TODO: select current session as a fallback
            res, key = self._rofi.select(rofi_msg, [
                "{}:{}:{}".format(w.session.name, w.index, w.name)
                for w in windows
            ])
            if key == 0:
                win = windows[res]
                if action == 'switch':
                    self.logger.debug('selected: {}:{}:{}'.format(
                        win.session.name, win.index, win.name))
                    if self._has_i3:
                        self._switch_i3_tmux_workspace(
                            windows[res].session.name)
                    try:
                        self.logger.debug('tmux switching: {}'.format(
                            win.session.name))
                        win.session.switch_client()
                        win.select_window()
                    except libtmux.exc.LibTmuxException as e:
                        # there are no attached clients yet
                        self.logger.debug('tmux attaching: {}'.format(
                            win.session.name))
                        win.session.attach_session()
                elif action == 'kill':
                    win.kill_window()
                else:
                    self._rofi.error('This action is not implemented')

    def switch_window(self, session_name=None, global_scope=True) -> None:
        """Switches to a window of a particular session or any session

        :session_name: if it's not None, the scope is limited to this session
        :global_scope: if True, it will take into account all existent windows

        """
        self._rofi_tmux_window(
            action='switch',
            rofi_msg='Switch window: ',
            session_name=session_name,
            global_scope=global_scope)

    def kill_window(self, session_name=None, global_scope=True) -> None:
        """Kills window of a particular session or any session

        :session_name: if it's not None, the scope is limited to this session
        :global_scope: if True, it will take into account all existent windows

        """
        self._rofi_tmux_window(
            action='kill',
            rofi_msg='Kill window: ',
            session_name=session_name,
            global_scope=global_scope)
