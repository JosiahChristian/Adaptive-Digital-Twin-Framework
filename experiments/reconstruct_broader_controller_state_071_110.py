from pathlib import Path

import experiments.cross_seed_harmful_expansion_feature_decomposition as source


TARGET_SEEDS = list(
    range(
        44071,
        44111,
    )
)

SUMMARY_OUTPUT_PATH = Path(
    "results/"
    "cross_seed_harmful_expansion_feature_decomposition_071_110.csv"
)

EVENT_OUTPUT_PATH = Path(
    "results/"
    "cross_seed_harmful_expansion_feature_decomposition_events_071_110.csv"
)


def find_seed_attribute():
    candidates = [
    "BASE_GENERATION_SEEDS",
    "ANALYSIS_SEEDS",
    "GENERATION_SEEDS",
    "SEEDS",
]

    for name in candidates:
        if hasattr(
            source,
            name,
        ):
            value = getattr(
                source,
                name
            )

            if isinstance(
                value,
                (
                    list,
                    tuple,
                    range,
                ),
            ):
                return name

    raise RuntimeError(
        "Could not identify the source module's seed-list attribute. "
        "Reconstruction stopped rather than modifying an unknown setting."
    )


def find_output_attributes():
    discovered = {}

    for name, value in vars(
        source
    ).items():
        if not isinstance(
            value,
            Path,
        ):
            continue

        lower_name = name.lower()
        lower_path = str(
            value
        ).lower()

        if (
            "output" in lower_name
            or "result" in lower_name
        ):
            discovered[
                name
            ] = value

        elif (
            "cross_seed_harmful_expansion_feature_decomposition"
            in lower_path
        ):
            discovered[
                name
            ] = value

    return discovered


def replacement_path(
    original,
):
    name = original.name

    if (
        "events"
        in name.lower()
    ):
        return EVENT_OUTPUT_PATH

    if name == (
        "cross_seed_harmful_expansion_feature_decomposition.csv"
    ):
        return SUMMARY_OUTPUT_PATH

    stem = original.stem

    if stem.endswith(
        "_071_110"
    ):
        return original

    return original.with_name(
        f"{stem}_071_110"
        f"{original.suffix}"
    )


def main():
    print(
        "=" * 210
    )

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "BROADER CONTROLLER-STATE RECONSTRUCTION 44071-44110"
    )

    print(
        "=" * 210
    )

    print(
        "source module="
        "experiments.cross_seed_harmful_expansion_feature_decomposition"
    )

    print(
        "target seeds=44071-44110"
    )

    print(
        f"seed count="
        f"{len(TARGET_SEEDS)}"
    )

    print()

    seed_attribute = (
        find_seed_attribute()
    )

    output_attributes = (
        find_output_attributes()
    )

    print(
        f"source seed attribute="
        f"{seed_attribute}"
    )

    print()

    print(
        "DISCOVERED SOURCE OUTPUTS"
    )

    if not output_attributes:
        raise RuntimeError(
            "No source output Path attributes were discovered. "
            "Reconstruction stopped before executing the source module."
        )

    for name, path in sorted(
        output_attributes.items()
    ):
        print(
            f"{name}={path}"
        )

    original_seed_value = getattr(
        source,
        seed_attribute,
    )

    original_outputs = dict(
        output_attributes
    )

    try:
        setattr(
            source,
            seed_attribute,
            list(
                TARGET_SEEDS
            ),
        )

        print()

        print(
            "RECONSTRUCTION OUTPUTS"
        )

        for name, original_path in sorted(
            output_attributes.items()
        ):
            new_path = replacement_path(
                original_path
            )

            setattr(
                source,
                name,
                new_path,
            )

            print(
                f"{name}={new_path}"
            )

        print()

        print(
            "=" * 210
        )

        print(
            "REUSING ESTABLISHED CROSS-SEED HARMFUL-EXPANSION "
            "FEATURE-DECOMPOSITION IMPLEMENTATION"
        )

        print(
            "=" * 210
        )

        source.main()

    finally:
        setattr(
            source,
            seed_attribute,
            original_seed_value,
        )

        for name, original_path in (
            original_outputs.items()
        ):
            setattr(
                source,
                name,
                original_path,
            )

    print()

    if not EVENT_OUTPUT_PATH.exists():
        raise RuntimeError(
            "Expected reconstructed event file was not generated: "
            f"{EVENT_OUTPUT_PATH}"
        )

    print(
        "RECONSTRUCTION COMPLETE"
    )

    print(
        "The broader controller-state representation was generated "
        "using the existing cross-seed harmful-expansion feature-"
        "decomposition implementation with only its analysis seed "
        "population and output destinations changed."
    )

    print(
        "No Experiment 118 action-harm model was fit during this "
        "reconstruction."
    )

    print(
        "=" * 210
    )


if __name__ == "__main__":
    main()