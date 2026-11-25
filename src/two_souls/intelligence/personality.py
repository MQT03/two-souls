import math
from dataclasses import dataclass, field
from typing import TypeAlias


TraitValue: TypeAlias = bool | int | float | str


@dataclass(frozen=True)
class TraitDefinition:
    """Defines the type and optional numeric bounds for a personality trait."""

    name: str
    value_type: type
    minimum: int | float | None = None
    maximum: int | float | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Trait name cannot be empty.")

        if self.value_type not in (bool, int, float, str):
            raise TypeError("Unsupported trait value type.")

        for bound in (self.minimum, self.maximum):
            if bound is not None and (
                isinstance(bound, bool) or not isinstance(bound, (int, float))
            ):
                raise TypeError("Trait bounds must be numeric.")
        if (
            (self.minimum is not None or self.maximum is not None)
            and self.value_type not in (int, float)
        ):
            raise TypeError("Only numeric traits can have numeric bounds.")

        if (
            self.minimum is not None
            and self.maximum is not None
            and self.minimum > self.maximum
        ):
            raise ValueError("Trait minimum cannot exceed its maximum.")


@dataclass(frozen=True)
class TraitInstance:
    """A value for a trait definition owned by one agent's personality."""

    definition: TraitDefinition
    value: TraitValue

    def __post_init__(self) -> None:
        if not isinstance(self.definition, TraitDefinition):
            raise TypeError("Trait definition must be a TraitDefinition.")

        if self.definition.value_type is bool:
            valid_type = type(self.value) is bool
        elif self.definition.value_type is int:
            valid_type = type(self.value) is int
        elif self.definition.value_type is float:
            valid_type = (
                isinstance(self.value, (int, float))
                and not isinstance(self.value, bool)
            )
        else:
            valid_type = type(self.value) is str

        if not valid_type:
            raise TypeError(
                f"Trait '{self.definition.name}' must have value type "
                f"{self.definition.value_type.__name__}."
            )

        if isinstance(self.value, (int, float)) and not isinstance(
            self.value, bool
        ):
            if not math.isfinite(self.value):
                raise ValueError(
                    f"Trait '{self.definition.name}' must be finite."
                )
            if (
                self.definition.minimum is not None
                and self.value < self.definition.minimum
            ):
                raise ValueError(
                    f"Trait '{self.definition.name}' is below its minimum."
                )
            if (
                self.definition.maximum is not None
                and self.value > self.definition.maximum
            ):
                raise ValueError(
                    f"Trait '{self.definition.name}' exceeds its maximum."
                )


def _default_traits() -> dict[str, TraitInstance]:
    return {
        name: TraitInstance(
            TraitDefinition(name, float, minimum=0.0, maximum=100.0),
            50.0,
        )
        for name in ("sociability", "kindness", "curiosity", "diligence")
    }


@dataclass
class Personality:
    """A flexible collection of typed trait instances."""

    traits: dict[str, TraitInstance] = field(default_factory=_default_traits)

    def __post_init__(self) -> None:
        for name, trait in self.traits.items():
            if not isinstance(trait, TraitInstance):
                raise TypeError("Personality traits must be TraitInstances.")
            if name != trait.definition.name:
                raise ValueError("Trait key must match its definition name.")

    @classmethod
    def with_traits(
        cls,
        traits: dict[str, TraitInstance],
    ) -> "Personality":
        combined = _default_traits()
        combined.update(traits)
        return cls(combined)

    def get_trait(self, name: str) -> TraitInstance:
        return self.traits[name]

    def numeric_value(self, name: str) -> float:
        value = self.get_trait(name).value
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Trait '{name}' must have a numeric value.")
        return float(value)
