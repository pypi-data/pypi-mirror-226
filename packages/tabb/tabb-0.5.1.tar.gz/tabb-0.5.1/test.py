import dataclasses
import json
import pathlib
from collections.abc import Callable
from typing import Annotated, Any, Literal, ParamSpec, TypeVar

from tabb.callback import register_callback
from tabb.context import Context
from tabb.decorators import group
from tabb.parameter.types import Counter, List, Path
from tabb.types import Argument, Depends, Length, Option

T = TypeVar("T")
P = ParamSpec("P")


def load_json_config(
    *flags: str,
    default: str = "config.json",
    show_default: bool = True,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    if not flags:
        flags = ("--config",)

    localns = locals()

    def update_config(
        ctx: Context[Any],
        filename: Annotated[
            str, Option(*flags, default=default, show_default=show_default)
        ],
    ) -> None:
        try:
            with open(filename) as f:
                data = json.load(f)
        except Exception as error:
            print(f"Error loading config file: {error}")

        else:
            ctx.config.merge(data)

    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        register_callback(fn, update_config, localns=localns)
        return fn

    return decorator


@group()
# @load_json_config()
def cli(foo: bool | None = None) -> None:
    print(f"{foo=}")


@cli.command
def cp(
    src: Annotated[
        list[pathlib.Path],
        Argument(type=List(Path(exists=True, readable=True), nargs="*")),
        Length(min=0, max=2),
    ],
    dest: pathlib.Path,
    verbose: Annotated[int, Option("-v", "--verbose", type=Counter())] = False,
) -> None:
    print(f"{src=} {dest=} {verbose=}")


@cli.command
def test_types(ints: list[int], strs: list[str]) -> None:
    print(f"{ints=} {strs=}")


@cli.command
def test_parameters(
    pos_only: str | None = None,
    /,
    pos_or_kw: str | None = None,
    *var_pos: int,
    kw_only: str | None = None,
    **var_kw: int,
) -> None:
    print(f"{pos_only=} {pos_or_kw=} {var_pos=} {kw_only=} {var_kw=}")


def get_home(ctx: Context[Any]) -> str | None:
    return ctx.environ.get("HOME")


def get_email(username: str | None = None, domain: str | None = None) -> str | None:
    if username is None or domain is None:
        return None
    return f"{username}@{domain}"


def higher_order_dep(
    home: Annotated[str | None, Depends(get_home)],
    email: Annotated[str | None, Depends(get_email)],
) -> str:
    return f"{home=} {email=}"


@dataclasses.dataclass
class User:
    name: str | None = None
    email: Annotated[str | None, Depends(get_email)] = None


@cli.command
def test_depends(
    ctx: Context[None],
    user: User,
    home: Annotated[str | None, Depends(get_home)],
    email: Annotated[str | None, Depends(get_email)],
    hod: Annotated[str, Depends(higher_order_dep)],
) -> None:
    print(f"{ctx=} {home=} {email=} {hod=} {user=}")


@cli.command
def hello(
    name: Annotated[str, Argument(default="World")],
    greeting: Annotated[
        str, Option(show_default=True, show_config=True, show_envvar=True)
    ] = "Hello",
    debug: Annotated[bool, Option(show_default=True)] = False,
    things: Annotated[list[str] | None, Option(help="Just some things.")] = None,
    repeat: Annotated[
        int, Option("-n", "--repeat", help="Number of times to repeat.")
    ] = 1,
) -> None:
    """Say hello."""
    for _ in range(repeat):
        print(f"{greeting} {name}!")
    print(f"Things: {things}")


@cli.command()
def train(
    # The training data
    examples_path: str,
    # Model options
    base_model: Annotated[str, Option()],
    tokenizer: Annotated[str, Option()],
    skills_path: Annotated[str, Option()],
    output_dir: str = "/defaut/output/path",
    # Training options
    seed: int = 42,
    max_seq_length: int = 128,
    logger: Literal["csv", "tensorboard"] = "csv",
    max_epocs: int = 1,
    gradient_accumulation_steps: int = 8,
    val_check_interval: int = 1000,
    train_batch_size: int = 4,
    eval_batch_size: int = 4,
    learning_rate: float = 1e-3,
    lr_start_factor: float = 1.0,
    lr_end_factor: float = 0.1,
    lr_scheduler_frequency: int = 1,
    no_grad: tuple[str, ...] = (),
) -> None:
    print(80 * "=")
    for key, value in locals().items():
        print(f"{key}={value}")


@cli.command()
async def test_async() -> None:
    print("test_async")


if __name__ == "__main__":
    cli(auto_config_prefix="cli", auto_envvar_prefix="CLI")
