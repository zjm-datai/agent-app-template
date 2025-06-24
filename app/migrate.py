# migrate.py
import os
import click
from alembic.config import Config
from alembic import command

# 假设 alembic.ini 与此脚本同级
ALEMBIC_INI_PATH = os.path.join(os.path.dirname(__file__), "alembic.ini")

def get_config() -> Config:
    cfg = Config(ALEMBIC_INI_PATH)
    return cfg

@click.group()
def cli():
    """FastAPI + SQLModel 数据库迁移工具（基于 Alembic）"""
    pass

@cli.command()
def init():
    """
    初始化 Alembic 目录（只需执行一次）
    """
    cfg = get_config()
    # alembic.command.init 里第一个参数是 Config，第二个是脚本目录
    script_location = cfg.get_main_option("script_location")
    command.init(cfg, script_location)
    click.echo("Alembic initialized.")

@cli.command()
@click.option("-m", "--message", required=True, help="本次迁移的描述信息")
def revision(message: str):
    """
    自动生成一个迁移脚本
    """
    cfg = get_config()
    command.revision(cfg, message=message, autogenerate=True)
    click.echo(f"Revision created: '{message}'")

@cli.command()
@click.argument("revision", default="head", required=False)
def upgrade(revision: str):
    """
    将数据库升级到指定版本（默认为 head）
    """
    cfg = get_config()
    command.upgrade(cfg, revision)
    click.echo(f"Upgraded to {revision}")

@cli.command()
@click.argument("revision", required=True)
def downgrade(revision: str):
    """
    将数据库降级到指定版本（如 -1、<revision_id> 等）
    """
    cfg = get_config()
    command.downgrade(cfg, revision)
    click.echo(f"Downgraded to {revision}")

if __name__ == "__main__":
    cli()
