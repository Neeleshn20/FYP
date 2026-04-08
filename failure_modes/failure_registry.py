from failure_modes.signal_delay import apply as signal_delay
from failure_modes.demand_drift import apply as demand_drift
from failure_modes.holiday_amplification import apply as holiday_amplification
from failure_modes.cluster_regime_shift import apply as cluster_regime_shift
from failure_modes.department_coupling_distortion import apply as department_coupling_distortion
from failure_modes.resource_concentration import apply as resource_concentration
from failure_modes.feedback_amplification import apply as feedback_amplification
from failure_modes.systematic_bias import apply as systematic_bias
from failure_modes.myopic_policy import apply as myopic_policy


FAILURES = {
    "Signal Delay": signal_delay,
    "Demand Drift": demand_drift,
    "Holiday Amplification": holiday_amplification,
    "Cluster Regime Shift": cluster_regime_shift,
    "Department Coupling Distortion": department_coupling_distortion,
    "Resource Concentration": resource_concentration,
    "Feedback Amplification": feedback_amplification,
    "Systematic Bias": systematic_bias,
    "Myopic Decision Policy": myopic_policy
}
