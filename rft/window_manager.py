#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class WindowManager(ABC):
    """Window Manager Abstract Class"""

    def __init__(self):
        """Constructor

        """
        super(WindowManager, self).__init__()

    @abstractmethod
    def switch_tmux_workspace(self) -> None:
        """Switches to the workspace where tmux session_name is running

        """
        pass

    @abstractmethod
    def is_tmux_not_in_cur_workspace(self, session_name) -> bool:
        """Verifies if tmux is not in the cur workspace

        """
        pass
