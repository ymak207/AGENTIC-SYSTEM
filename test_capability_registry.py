from orchestrator.workflow import run_workflow


queries = [

    "Explain Docker",

    "23*44",

    "What is my profession"

]


for query in queries:

    print("=" * 80)
    print(query)
    print("=" * 80)

    state = run_workflow(query)

    # ====================================================
    # Basic validations
    # ====================================================

    assert state is not None

    assert state.final_answer
    assert len(state.final_answer.strip()) > 0

    assert state.plan is not None
    assert "goal" in state.plan
    assert "steps" in state.plan
    assert len(state.plan["steps"]) > 0

    assert isinstance(state.metrics, dict)

    assert isinstance(state.trace, list)
    assert len(state.trace) > 0

    assert state.workflow_status is not None

    assert isinstance(state.knowledge, dict)

    # ====================================================
    # Knowledge validation
    # ====================================================

    if "Docker" in query:

        assert (
            len(state.knowledge["memory"])
            + len(state.knowledge["rag"])
            + len(state.knowledge["web"])
        ) > 0

    # ====================================================
    # Compute validation
    # ====================================================

    if "23*44" in query:

        assert len(state.compute_results) == 1

        result = state.compute_results[0]

        assert result["expression"] == "23*44"

        assert float(result["result"]) == 1012

    # ====================================================
    # Print Results
    # ====================================================

    print("\nAnswer\n")
    print(state.final_answer)

    print("\nMetrics\n")
    print(state.metrics)

    print("\nTrace\n")
    print(state.trace)

    print("\nKnowledge\n")
    print(state.knowledge)

    if state.compute_results:

        print("\nCompute Results\n")
        print(state.compute_results)

    print()

print("\nWorkflow test passed.")