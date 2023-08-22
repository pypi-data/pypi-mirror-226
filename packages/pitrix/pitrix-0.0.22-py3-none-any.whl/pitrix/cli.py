#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import os
import click
from emoji import emojize
from click_help_colors import HelpColorsGroup, version_option

from pitrix.utils.log import pitrix_logger
from pitrix import __description__, __version__,__project__,__image__
from pitrix.scaffold import create_scaffold,delete_folder,create_virtual_environment

@click.group(cls=HelpColorsGroup,
             invoke_without_command=True,
             help_headers_color='magenta',
             help_options_color='green',
             context_settings={"max_content_width": 120, })
@version_option(version=__version__, prog_name=__project__, message_color="cyan")
@click.pass_context
def main(ctx):
    click.echo(__image__)
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@main.command()
@click.argument("project_name")
@click.option('--venv','-v',is_flag=True)
@click.pass_context
def startproject(ctx,project_name,venv):
    """创建一个新项目,例如:pitrix startproject demo,指定 -v 或者 --venv 来配置创建虚拟环境"""
    folder_path = os.path.join(os.getcwd(), project_name)
    ctx.obj['project_path'] = folder_path
    create_scaffold(project_name)
    click.echo(emojize(":beer_mug: 项目脚手架创建完成！"))

    if venv:
        # create_virtual_environment(ctx.obj['project_path'])
        create_virtual_environment(project_name)

@main.command()
@click.argument("project_name")
@click.pass_context
def deleteproject(ctx,project_name):
    """删除一个项目,例如:pitrix deleteproject demo"""
    folder_path = os.path.join(os.getcwd(), project_name)
    pitrix_logger.info(f"folder_path:{folder_path}")
    delete_folder(project_name)


if __name__ == '__main__':
    main()