from failure_modes import (
    signal_delay,
    demand_drift,
    holiday_amplification,
    cluster_regime_shift,
    department_coupling_distortion,
    resource_concentration,
    feedback_amplification,
    systematic_bias,
    myopic_policy
)

FAILURE_MAP = {
    "signal_delay": signal_delay.apply,
    "demand_drift": demand_drift.apply,
    "holiday_amplification": holiday_amplification.apply,
    "cluster_regime_shift": cluster_regime_shift.apply,
    "department_coupling": department_coupling_distortion.apply,
    "resource_concentration": resource_concentration.apply,
    "feedback_amplification": feedback_amplification.apply,
    "systematic_bias": systematic_bias.apply,
    "myopic_policy": myopic_policy.apply
}


def generate_failure(df, failure_type, **params):

    if failure_type not in FAILURE_MAP:
        raise ValueError(f"Unknown failure: {failure_type}")

    return FAILURE_MAP[failure_type](df, **params)


def load_data(df_base, failure_type=None, **params):

    if failure_type is None:
        return df_base.copy()

    return generate_failure(df_base, failure_type, **params)