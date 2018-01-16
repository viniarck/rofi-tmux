#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import rofi_tmux.rofi_tmux as rt
import rofi_tmux.version as v


@click.group()
@click.pass_context
@click.option(
    '--debug',
    default=False,
    type=bool,
    help='Enables logging at debug level')
def main(ctx, debug):
    ctx.obj = rt.RofiTmux(debug=debug)


@main.command()
@click.pass_obj
def switch_session(ctx):
    ctx.switch_session()


@main.command()
@click.pass_obj
def kill_session(ctx):
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
def switch_window(ctx, session_name, global_scope):
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
def kill_window(ctx, session_name, global_scope):
    ctx.kill_window(session_name=session_name, global_scope=global_scope)


@main.command()
@click.pass_obj
def load_project(ctx):
    ctx.load_tmuxinator()


@main.command()
def version():
    print(v.__version__)


if __name__ == "__main__":
    main()
