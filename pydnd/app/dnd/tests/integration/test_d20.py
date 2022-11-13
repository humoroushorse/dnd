"""A d20 roll to add some excitement to our tests."""
import random


def test_roll_d20(skip_d20: bool) -> None:
    """A test that only fails if you roll a nat 1.

    This can be overridden with the custom pytest flag `--skip-d20=True`

    Args:
        skip_d20 (bool): Custom pytest flag --skip-d20. Defaults to False.
    """
    if not skip_d20:
        roll = random.randint(1, 20)
        print(f"D20 result: {roll}")  # noqa: T001
        assert roll > 1, "Oh no, you rolled a nat 1! Critical Fail!"
