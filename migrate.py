# migrate.py
import os
import click
from alembic.config import Config
from alembic import command

# 假设 alembic.ini 与此脚本同级
ALEMBIC_INI_PATH = os.path.join(os.path.dirname(__file__), "alembic.ini")

def get_config() -> Config:
    # 加载 Alembic 配置文件
    cfg = Config(ALEMBIC_INI_PATH)
    return cfg

@click.group()
def cli():
    """FastAPI + SQLModel 数据库迁移工具（基于 Alembic）"""
    pass


@cli.command()
def init():
    """
    初始化 Alembic 目录结构（只需执行一次）
    等价于：alembic init <script_location>
    """
    cfg = get_config()
    # 获取配置中的 script_location，比如 "alembic"
    script_location = cfg.get_main_option("script_location")
    # 创建目录结构，生成 env.py、versions/ 等
    command.init(cfg, script_location)
    click.echo("Alembic initialized.")


@cli.command()
@click.option("-m", "--message", required=True, help="本次迁移的描述信息")
def revision(message: str):
    """
    自动生成一个迁移脚本（对比模型与数据库差异）
    等价于：alembic revision --autogenerate -m "<message>"
    """
    cfg = get_config()
    # autogenerate=True 会基于 metadata 自动检测差异生成脚本
    command.revision(cfg, message=message, autogenerate=True)
    click.echo(f"Revision created: '{message}'")


@cli.command()
@click.argument("revision", default="head", required=False)
def upgrade(revision: str):
    """
    将数据库升级到指定版本（默认为 head，即最新）
    等价于：alembic upgrade <revision>
    示例：
        python migrate.py upgrade        # 等价于 alembic upgrade head
        python migrate.py upgrade abc123def456
    """
    cfg = get_config()
    command.upgrade(cfg, revision)
    click.echo(f"Upgraded to {revision}")


@cli.command()
@click.argument("revision", required=True)
def downgrade(revision: str):
    """
    将数据库降级到指定版本（如 -1、<revision_id> 等）
    等价于：alembic downgrade <revision>
    示例：
        python migrate.py downgrade -1           # 回退一个版本
        python migrate.py downgrade abc123def456 # 降级到某个版本
    """
    cfg = get_config()
    command.downgrade(cfg, revision)
    click.echo(f"Downgraded to {revision}")


if __name__ == "__main__":
    # 允许通过命令行执行脚本，例如：python migrate.py upgrade
    cli()
