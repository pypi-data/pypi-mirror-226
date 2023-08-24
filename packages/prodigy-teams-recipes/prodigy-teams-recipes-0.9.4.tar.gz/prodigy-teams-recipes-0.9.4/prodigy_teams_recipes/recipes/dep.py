from typing import List, Literal

import prodigy.recipes.dep
from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import Dataset, Goal, Input, UseModel, props, task_recipe


@task_recipe(
    title="Dependency Parsing",
    description="Annotate syntactic dependencies.",
    view_id="relations",
    field_props={
        "dataset": props.dataset_choice,
        "label": props.label,
        "model": props.model,
        "segment": props.segment,
        "goal": props.goal,
    },
)
def dep(
    *,
    dataset: Dataset[Literal["dep"]],
    model: UseModel,
    input: Input,
    label: List[str],
    segment: bool = False,
    goal: Goal = "nooverlap",
) -> RecipeSettingsType:
    if isinstance(model, UseModel):
        spacy_model = model.name
        update_model = model.update
    else:
        spacy_model = model.lang
        update_model = False
    assert spacy_model.path is not None
    nlp = spacy_model.load()
    stream = input.load(rehash=True, dedup=True, input_key="text")
    labels = prodigy.recipes.dep.get_dep_labels(nlp, label)
    stream = prodigy.recipes.dep.preprocess_stream(
        stream, nlp, unsegmented=not segment, labels=labels
    )

    return {
        "dataset": dataset.name,
        "stream": stream,
        "update": prodigy.recipes.dep.get_update(nlp) if update_model else None,
        "view_id": "relations",
        "config": {
            "lang": nlp.lang,
            "labels": label,
            "feed_overlap": goal == "overlap",
            "custom_theme": {"cardMaxWidth": "90%", "relationHeight": 150},
        },
    }
