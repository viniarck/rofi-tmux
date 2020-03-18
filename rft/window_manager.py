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
    def focus_tmux_window(self, session) -> None:

        """Focuses window where given tmux session is running in

        """
        pass

    @abstractmethod
    def is_tmux_win_visible(self, session) -> bool:
        """Verifies if window where given tmux session is running in is visible

        """
        pass
