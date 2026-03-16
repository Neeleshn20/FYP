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

    "Signal Delay": {
        "function": signal_delay,
        "parameter": "delay_weeks",
        "ui": {
            "type": "number_input",
            "label": "Signal Delay (weeks)",
            "min": 1,
            "max": 12,
            "default": 4
        }
    },

    "Demand Drift": {
        "function": demand_drift,
        "parameter": "drift_rate",
        "ui": {
            "type": "slider",
            "label": "Demand Drift Rate",
            "min": 0.0,
            "max": 0.02,
            "default": 0.002,
            "step": 0.001
        }
    },

    "Holiday Amplification": {
        "function": holiday_amplification,
        "parameter": "drift_strength",
        "ui": {
            "type": "slider",
            "label": "Holiday Noise Strength",
            "min": 0.0,
            "max": 1.0,
            "default": 0.3,
            "step": 0.05
        }
    },

    "Cluster Regime Shift": {
        "function": cluster_regime_shift,
        "parameter": "severity",
        "ui": {
            "type": "slider",
            "label": "Cluster Regime Strength",
            "min": 0.0,
            "max": 1.0,
            "default": 0.4,
            "step": 0.05
        }
    },

    "Department Coupling Distortion": {
        "function": department_coupling_distortion,
        "parameter": "severity",
        "ui": {
            "type": "slider",
            "label": "Coupling Distortion Strength",
            "min": 0.0,
            "max": 1.0,
            "default": 0.3,
            "step": 0.05
        }
    },

    "Resource Concentration": {
        "function": resource_concentration,
        "parameter": "severity",
        "ui": {
            "type": "slider",
            "label": "Resource Concentration",
            "min": 0.1,
            "max": 1.0,
            "default": 0.5,
            "step": 0.05
        }
    },

    "Feedback Amplification": {
        "function": feedback_amplification,
        "parameter": "feedback_strength",
        "ui": {
            "type": "number_input",
            "label": "Amplification Factor",
            "min": 1.0,
            "max": 10.0,
            "default": 2.0
        }
    },

    "Systematic Bias": {
        "function": systematic_bias,
        "parameter": "bias_strength",
        "ui": {
            "type": "number_input",
            "label": "Forecast Bias",
            "min": -0.5,
            "max": 0.5,
            "default": 0.1
        }
    },

    "Myopic Decision Policy": {
        "function": myopic_policy,
        "parameter": "lookback_weeks",
        "ui": {
            "type": "number_input",
            "label": "Lookback Window",
            "min": 1,
            "max": 12,
            "default": 2
        }
    }
}