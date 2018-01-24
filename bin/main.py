#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import rft.rft as rft
import rft.version as version


@click.group()
@click.pass_context
@click.option(
    '--debug',
    default=False,
    type=bool,
    help='Enables logging at debug level.')
def main(ctx, debug):
    """RFT (rofi-tmux) switcher."""
    ctx.obj = rft.RFT(debug=debug)


@main.command()
@click.pass_obj
def ss(ctx):
    """Switch tmux session.

    :param ctx: context
    """
    ctx.switch_session()


@main.command()
@click.pass_obj
def ks(ctx):
    """Kill tmux session.

    :param ctx: context
    """
    ctx.kill_session()


@main.command()
@click.option(
    '--session_name',
    default=None,
    help='limit the scope to this this sesison')
@click.option(
    '--global_scope',
    default=True,
    type=bool,
    help='true, if you want to consider all windows')
@click.pass_obj
def sw(ctx, session_name, global_scope):
    """Switch tmux window.

    :param ctx: context
    :param session_name: tmux session name
    :param global_scope: True to consider all windows
    """
    ctx.switch_window(session_name=session_name, global_scope=global_scope)


@main.command()
@click.option(
    '--session_name',
    default=None,
    help='limit the scope to this this sesison')
@click.option(
    '--global_scope',
    default=True,
    type=bool,
    help='true, if you want to consider all windows')
@click.pass_obj
def kw(ctx, session_name, global_scope):
    """Kill tmux window.

    :param ctx: context
    :param session_name: tmux session name
    :param global_scope: True to consider all windows
    """
    ctx.kill_window(session_name=session_name, global_scope=global_scope)


@main.command()
@click.pass_obj
def lp(ctx):
    """Load tmuxinator project.

    :param ctx: context
    """
    ctx.load_tmuxinator()


@main.command()
def v():
    """Print version."""
    print(version.__version__)


if __name__ == "__main__":
    main()
