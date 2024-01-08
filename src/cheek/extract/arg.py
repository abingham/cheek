from dataclasses import dataclass, field


@dataclass
class Arg:
    name: str
    type: str
    default: str
    enum_values: list[str] = field(default_factory=list)

    @classmethod
    def from_spec(cls, spec: dict):
        enum_values = spec.get("enum", [])
        default_value = _default_value(spec["default"])
        return cls(
            name=spec["key"], type=spec["type"], default=default_value, enum_values=enum_values
        )


def _default_value(default_str):
    if default_str == "unchanged":
        return None
    return default_str
