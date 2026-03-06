"""muapi auth — configure API key and inspect identity."""
import typer
from rich.prompt import Prompt

from ..config import delete_api_key, get_api_key, save_api_key
from .. import exitcodes
from ..utils import console, error_exit, out

app = typer.Typer(help="Manage authentication and API key.")


@app.command("configure")
def configure(
    api_key: str = typer.Option(None, "--api-key", "-k", help="API key (will prompt if omitted)"),
):
    """Save your muapi API key to the OS keychain (or config file)."""
    if not api_key:
        api_key = Prompt.ask("[bold]Enter your muapi API key[/bold]", password=True, console=console)
    if not api_key:
        error_exit("No API key provided.")
    location = save_api_key(api_key.strip())
    console.print(f"[green]API key saved to {location}.[/green]")


@app.command("whoami")
def whoami():
    """Show the currently configured API key (masked)."""
    key = get_api_key()
    if not key:
        error_exit("No API key configured. Run: muapi auth configure", exitcodes.AUTH_ERROR)
    masked = key[:8] + "..." + key[-4:]
    out.print(f"API key: [bold]{masked}[/bold]")


@app.command("logout")
def logout():
    """Remove the stored API key."""
    delete_api_key()
    console.print("[green]API key removed.[/green]")
