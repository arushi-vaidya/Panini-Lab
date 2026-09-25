from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .core.derivation import DerivationEngine
from .core.experiment import CounterfactualExperiment
from .core.registry import RuleRegistry
from .core.sanskrit import tokenize_sanskrit
from .core.interaction_miner import InteractionMiner
from .core.dependency_graph import DependencyGraph
from .core.impact import RuleImpactAnalyzer
from .core.evaluation import EvaluationRunner


BASE_DIR = Path(__file__).resolve().parent

RULE_FILE = BASE_DIR / "data" / "rules.json"
EVALUATION_FILE = BASE_DIR / "data" / "evaluation_cases.json"


app = FastAPI(
    title="PĀṆINI-LAB",
    description=(
        "Counterfactual computational framework "
        "for Pāṇinian rule-dependency analysis."
    ),
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


registry = RuleRegistry()

registry.load_json(
    RULE_FILE
)

derivation_engine = DerivationEngine(registry.all_rules())

experiment_engine = CounterfactualExperiment(
    derivation_engine
)


class DerivationRequest(BaseModel):

    input_surface: str

    disabled_rules: list[str] = Field(default_factory=list)


class ExperimentRequest(BaseModel):

    input_surface: str

    disabled_rules: list[str] = Field(default_factory=list)
    rule_order: list[str] | None = None


class BatchExperimentRequest(BaseModel):
    input_surfaces: list[str] = Field(min_length=1)
    disabled_rules: list[str] = Field(default_factory=list)
    rule_order: list[str] | None = None


class InteractionRequest(BaseModel):
    input_surfaces: list[str] = Field(default_factory=list)


class ImpactRequest(BaseModel):
    input_surfaces: list[str] = Field(default_factory=list)


@app.get("/")
def root():

    return {
        "project": "PĀṆINI-LAB",
        "phase": "7",
        "status": "implemented_research_prototype",
        "capabilities": ["derivation", "counterfactuals", "impact_analysis", "dependency_graph", "interactive_visualization", "evaluation", "research_report"],
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
        "conditions": [condition.model_dump(mode="json") for condition in rule.conditions],
        "operations": [operation.model_dump(mode="json") for operation in rule.operations],
    }


@app.post("/derive")
def derive(
    request: DerivationRequest,
):

    unknown_rules = set(request.disabled_rules) - set(derivation_engine.get_rule_order())
    if unknown_rules:
        raise HTTPException(status_code=400, detail=f"Unknown rules: {sorted(unknown_rules)}")

    result = derivation_engine.derive(
        initial_state=tokenize_sanskrit(request.input_surface),
        disabled_rules=set(request.disabled_rules),
    )

    return {
        "input": result.input,
        "output": result.output,
        "halted": result.terminated_reason == "max_steps_reached",
        "halt_reason": result.terminated_reason,
        "applied_rules": result.fired_rules,
        "final_state": result.final_state.model_dump(),
        "trace": [step.to_dict() for step in result.steps],
    }


@app.post("/experiment")
def experiment(
    request: ExperimentRequest,
):

    known_rules = set(derivation_engine.get_rule_order())
    unknown_rules = set(request.disabled_rules) - known_rules
    if unknown_rules:
        raise HTTPException(status_code=400, detail=f"Unknown rules: {sorted(unknown_rules)}")
    if request.rule_order and set(request.rule_order) != known_rules:
        raise HTTPException(status_code=400, detail="rule_order must contain every known rule exactly once")

    result = experiment_engine.run(
        input_surface=request.input_surface,
        rules=registry.all_rules(),
        disabled_rules=request.disabled_rules,
        rule_order=request.rule_order,
    )

    return {
        "input": request.input_surface,
        "disabled_rules": result.disabled_rules,
        "baseline_output": result.baseline_output,
        "counterfactual_output": result.counterfactual_output,
        "output_changed": result.output_changed,
        "changed_steps": result.changed_steps,
        "impact_summary": result.impact_summary,
        "baseline_trace": [step.to_dict() for step in result.baseline.steps],
        "counterfactual_trace": [step.to_dict() for step in result.counterfactual.steps],
    }


@app.post("/experiments")
def batch_experiment(request: BatchExperimentRequest):
    payloads = []
    for input_surface in request.input_surfaces:
        payloads.append(experiment(ExperimentRequest(
            input_surface=input_surface,
            disabled_rules=request.disabled_rules,
            rule_order=request.rule_order,
        )))
    return {"count": len(payloads), "experiments": payloads}


@app.get("/graph")
def graph():
    return DependencyGraph(registry.all_rules()).to_dict()


def _mine_interactions(input_surfaces: list[str]):
    miner = InteractionMiner()
    for example in input_surfaces:
        miner.observe(derivation_engine.derive(tokenize_sanskrit(example)))
    return miner.to_dict()


@app.get("/interactions")
def interactions():
    return _mine_interactions(["अइ", "अउ", "इअ", "एअ", "अए"])


@app.post("/interactions")
def interactions_for_inputs(request: InteractionRequest):
    return _mine_interactions(request.input_surfaces or ["अइ", "अउ", "इअ", "एअ", "अए"])


@app.post("/impact")
def impact(request: ImpactRequest):
    inputs = request.input_surfaces or ["अइ", "इअ", "उअ", "एअ", "ओअ", "अउ", "अए", "अअ"]
    return RuleImpactAnalyzer(registry.all_rules(), inputs).analyze()


@app.get("/evaluation")
def evaluation():
    return EvaluationRunner.from_json(
        registry.all_rules(),
        EVALUATION_FILE,
    ).run()