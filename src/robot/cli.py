import typer
from typing import Annotated
from rich.console import Console
from rich import print
from rich.table import Table
from robot.robot_repository import RobotRepository
from robot.config import DatabaseConfig

app = typer.Typer(help="Robot Management System", no_args_is_help=True)
console = Console()


@app.callback()
def main(
    ctx: typer.Context,
    user: Annotated[
        str, typer.Option(envvar="PGUSER", help="Database user")
    ] = "postgres",
    password: Annotated[str, typer.Option(envvar="PGPASSWORD")] = "postgres",
    host: Annotated[str, typer.Option(envvar="PGHOST")] = "localhost",
    port: Annotated[str, typer.Option(envvar="PGPORT")] = "5432",
    db: Annotated[str, typer.Option(envvar="PGDATABASE")] = "postgres",
):
    """
    Manage database configuration
    """
    ctx.obj = {"host": host, "port": port, "user": user, "password": password, "db": db}


def get_db(ctx: typer.Context):
    """Get the database repository."""
    db_config = DatabaseConfig(
        host=ctx.obj["host"],
        port=ctx.obj["port"],
        user=ctx.obj["user"],
        password=ctx.obj["password"],
        db=ctx.obj["db"],
    )
    repo = RobotRepository(db_config.database_url)
    repo.init_db()
    return repo


@app.command()
def add(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", "-n", help="Name of the robot"),
    description: str = typer.Option(
        ..., "--description", "-d", help="Description of the robot"
    ),
):
    """Add a new robot to the system."""
    repo = get_db(ctx)
    try:
        robot_id = repo.add_robot(name, description)
        print(f"[green]✓ User created successfully with ID: {robot_id}[/green]")
    except Exception as e:
        print(f"[red]✗ Error creating user: {str(e)}[/red]")


@app.command()
def get(
    ctx: typer.Context,
    name: str = typer.Option(None, "--name", "-n", help="Name of the robot"),
    id: int = typer.Option(None, "--id", "-i", help="ID of the robot"),
):
    """Get robot by name or ID."""

    match (name, id):
        case (None, None):
            print("[red]Please provide either a name or an ID.[/red]")
            raise typer.Exit(1)
        case (str(), None):
            repo = get_db(ctx)
            robot = repo.get_robot_by_name(name)
        case (None, int()):
            repo = get_db(ctx)
            robot = repo.get_robot_by_id(id)

    match robot:
        case None:
            print(f"[red]No robot found with name or ID: {name or id}[/red]")
            raise typer.Exit(1)
        case _:
            table = Table(
                title="Robot Details", show_header=True, header_style="bold magenta"
            )
            table.add_column("ID", style="dim")
            table.add_column("Name", style="green")
            table.add_column("Description", style="blue")

            table.add_row(str(robot.id), robot.name, robot.description)
            console.print(table)


if __name__ == "__main__":
    app()
