from api_compose.root.models.session import SessionModel


def set_incremental_execution_id(session_model: SessionModel) -> SessionModel:
    for scenario_group in session_model.scenario_groups:
        for scenario in scenario_group.scenarios:
            cnt = 0
            for action in scenario.actions:
                cnt += 1
                action.execution_id = str(cnt)

    return session_model
