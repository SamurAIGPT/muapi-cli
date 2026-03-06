"""muapi auth — configure API key and inspect identity."""
import typer
import httpx
from rich.prompt import Prompt

from ..config import delete_api_key, get_api_key, save_api_key, BASE_URL
from .. import exitcodes
from ..utils import console, error_exit, out

app = typer.Typer(help="Manage authentication and API key.")

# Auth endpoints live at the root host, not under /api/v1
_AUTH_BASE = BASE_URL.replace("/api/v1", "")


@app.command("login")
def login(
    email: str = typer.Option(..., "--email", "-e", help="Your muapi.ai email address"),
    password: str = typer.Option(None, "--password", "-p", help="Password (will prompt if omitted)"),
):
    """Log in with email + password and save an API key automatically."""
    if not password:
        password = Prompt.ask("[bold]Password[/bold]", password=True, console=console)
    if not password:
        error_exit("Password is required.", exitcodes.AUTH_ERROR)

    try:
        resp = httpx.post(
            f"{_AUTH_BASE}/api/auth/cli/login",
            json={"email": email, "password": password, "username": ""},
            timeout=30.0,
        )
    except httpx.RequestError as exc:
        error_exit(f"Network error: {exc}", exitcodes.ERROR)

    if resp.status_code == 401:
        error_exit("Invalid email or password.", exitcodes.AUTH_ERROR)
    if resp.status_code == 403:
        error_exit("Email not verified. Check your inbox.", exitcodes.AUTH_ERROR)
    if resp.status_code >= 400:
        error_exit(f"Login failed: {resp.text}", exitcodes.AUTH_ERROR)

    data = resp.json()
    api_key = data.get("api_key", "")
    if not api_key:
        error_exit("No API key in response. Please try again.", exitcodes.AUTH_ERROR)

    location = save_api_key(api_key)
    console.print(f"[green]Logged in as {data.get('email', email)}. API key saved to {location}.[/green]")


@app.command("register")
def register(
    email: str = typer.Option(..., "--email", "-e", help="Email address to register"),
    password: str = typer.Option(None, "--password", "-p", help="Password (will prompt if omitted)"),
    username: str = typer.Option("", "--username", "-u", help="Display name (optional)"),
):
    """Create a new muapi.ai account and verify via email OTP."""
    if not password:
        password = Prompt.ask("[bold]Choose a password[/bold]", password=True, console=console)
        confirm = Prompt.ask("[bold]Confirm password[/bold]", password=True, console=console)
        if password != confirm:
            error_exit("Passwords do not match.", exitcodes.VALIDATION)
    if not password:
        error_exit("Password is required.", exitcodes.VALIDATION)

    try:
        resp = httpx.post(
            f"{_AUTH_BASE}/api/auth/register",
            json={"email": email, "password": password, "username": username or email.split("@")[0]},
            timeout=30.0,
        )
    except httpx.RequestError as exc:
        error_exit(f"Network error: {exc}", exitcodes.ERROR)

    if resp.status_code == 400:
        error_exit(f"Registration failed: {resp.json().get('detail', resp.text)}", exitcodes.VALIDATION)
    if resp.status_code >= 400:
        error_exit(f"Registration failed: {resp.text}", exitcodes.ERROR)

    detail = resp.json().get("detail", "OTP sent to your email.")
    console.print(f"[green]{detail}[/green]")
    console.print("Check your inbox, then run: [bold]muapi auth verify --email {email} --otp <OTP>[/bold]")


@app.command("verify")
def verify(
    email: str = typer.Option(..., "--email", "-e", help="Email address used during registration"),
    otp: str = typer.Option(..., "--otp", "-o", help="OTP code from your email"),
):
    """Verify your email OTP after registration, then save an API key."""
    try:
        resp = httpx.post(
            f"{_AUTH_BASE}/api/auth/verify-otp",
            json={"email": email, "otp": otp},
            timeout=30.0,
        )
    except httpx.RequestError as exc:
        error_exit(f"Network error: {exc}", exitcodes.ERROR)

    if resp.status_code == 401:
        error_exit("Invalid or expired OTP.", exitcodes.AUTH_ERROR)
    if resp.status_code >= 400:
        error_exit(f"Verification failed: {resp.text}", exitcodes.AUTH_ERROR)

    console.print("[green]Email verified! You can now log in.[/green]")
    console.print(f"Run: [bold]muapi auth login --email {email}[/bold]")


@app.command("forgot-password")
def forgot_password(
    email: str = typer.Option(..., "--email", "-e", help="Email address on your account"),
):
    """Send a password reset OTP to your email."""
    try:
        resp = httpx.post(
            f"{_AUTH_BASE}/api/auth/forgot-password",
            json={"email": email},
            timeout=30.0,
        )
    except httpx.RequestError as exc:
        error_exit(f"Network error: {exc}", exitcodes.ERROR)

    if resp.status_code == 404:
        error_exit("No account found for that email.", exitcodes.NOT_FOUND)
    if resp.status_code >= 400:
        error_exit(f"Request failed: {resp.text}", exitcodes.ERROR)

    console.print(f"[green]{resp.json().get('detail', 'OTP sent to your email.')}[/green]")
    console.print(f"Then run: [bold]muapi auth reset-password --email {email} --otp <OTP> --password <new>[/bold]")


@app.command("reset-password")
def reset_password(
    email: str = typer.Option(..., "--email", "-e", help="Your email address"),
    otp: str = typer.Option(..., "--otp", "-o", help="OTP from the reset email"),
    password: str = typer.Option(None, "--password", "-p", help="New password (will prompt if omitted)"),
):
    """Reset your password using an OTP sent to your email."""
    if not password:
        password = Prompt.ask("[bold]New password[/bold]", password=True, console=console)
        confirm = Prompt.ask("[bold]Confirm new password[/bold]", password=True, console=console)
        if password != confirm:
            error_exit("Passwords do not match.", exitcodes.VALIDATION)
    if not password:
        error_exit("Password is required.", exitcodes.VALIDATION)

    try:
        resp = httpx.post(
            f"{_AUTH_BASE}/api/auth/reset-password",
            json={"email": email, "otp": otp, "password": password},
            timeout=30.0,
        )
    except httpx.RequestError as exc:
        error_exit(f"Network error: {exc}", exitcodes.ERROR)

    if resp.status_code == 401:
        error_exit("Invalid or expired OTP.", exitcodes.AUTH_ERROR)
    if resp.status_code >= 400:
        error_exit(f"Request failed: {resp.text}", exitcodes.ERROR)

    console.print(f"[green]{resp.json().get('detail', 'Password reset successfully.')}[/green]")
    console.print(f"Run: [bold]muapi auth login --email {email}[/bold]")


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
