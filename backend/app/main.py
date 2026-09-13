from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .core.derivation import DerivationEngine
from .core.experiment import CounterfactualExperiment
from .core.registry import RuleRegistry


BASE_DIR = Path(__file__).resolve().parent

RULE_FILE = BASE_DIR / "data" / "rules.json"


app = FastAPI(
    title="PĀṆINI-LAB",
    description=(
        "Counterfactual computational framework "
        "for Pāṇinian rule-dependency analysis."
    ),
    version="0.2.0",
)


registry = RuleRegistry()

registry.load_json(
    RULE_FILE
)

derivation_engine = DerivationEngine()

experiment_engine = CounterfactualExperiment(
    derivation_engine
)


class DerivationRequest(BaseModel):

    input_surface: str

    disabled_rules: list[str] = []


class ExperimentRequest(BaseModel):

    input_surface: str

    disabled_rules: list[str]


@app.get("/")
def root():

    return {
        "project": "PĀṆINI-LAB",
        "phase": "1B",
        "status": "implemented",
    }


@app.get("/rules")
def get_rules():

    return {
        "count": len(
            registry.all_rules()
        ),
        "rules": [
            {
                "rule_id": rule.rule_id,
                "sutra": rule.sutra,
                "name": rule.name,
                "priority": rule.priority,
                "enabled": rule.enabled,
                "status": rule.status,
            }
            for rule in registry.all_rules()
        ],
    }


@app.get("/rules/{rule_id}")
def get_rule(
    rule_id: str,
):

    try:

        rule = registry.get(
            rule_id
        )

    except KeyError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return {
        "rule_id": rule.rule_id,
        "sutra": rule.sutra,
        "name": rule.name,
        "description": rule.description,
        "priority": rule.priority,
        "status": rule.status,
        "enabled": rule.enabled,
        "conditions": [
            condition.__dict__
            for condition in rule.conditions
        ],
        "operations": [
            operation.__dict__
            for operation in rule.operations
        ],
    }


@app.post("/derive")
def derive(
    request: DerivationRequest,
):

    result = derivation_engine.derive(
        input_surface=request.input_surface,
        rules=registry.all_rules(),
        disabled_rules=request.disabled_rules,
    )

    return {
        "input": result.input_surface,
        "output": result.output_surface,
        "halted": result.halted,
        "halt_reason": result.halt_reason,
        "applied_rules": result.applied_rules,
        "final_state": result.final_state.snapshot(),
        "trace": [
            record.__dict__
            for record in result.records
        ],
    }


@app.post("/experiment")
def experiment(
    request: ExperimentRequest,
):

    result = experiment_engine.run(
        input_surface=request.input_surface,
        rules=registry.all_rules(),
        disabled_rules=request.disabled_rules,
    )

    return {
        "input": request.input_surface,
        "disabled_rules": result.disabled_rules,
        "baseline_output": result.baseline_output,
        "counterfactual_output": result.counterfactual_output,
        "output_changed": result.output_changed,
        "changed_steps": result.changed_steps,
        "impact_summary": result.impact_summary,
    }