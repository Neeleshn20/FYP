PARAM_GRID = {

    "Signal Delay": {
        "param": "delay_weeks",
        "values": [2, 4, 8,10]
    },

    "Demand Drift": {
        "param": "drift_rate",
        "values": [0.002, 0.006, 0.01, 0.02,0.04, 0.05]
    },

    "Holiday Amplification": {
        "param": "drift_strength",
        "values": [0.2, 0.4, 0.6, 0.8]
    },

    "Cluster Regime Shift": {
        "param": "severity",
        "values": [0.2, 0.4, 0.6, 0.8]
    },

    "Department Coupling Distortion": {
        "param": "severity",
        "values": [0.3, 0.6,0.45, 0.9]
    },

    "Resource Concentration": {
        "param": "severity",
        "values": [0.3, 0.6,0.45, 0.9]
    },

    "Feedback Amplification": {
        "param": "feedback_strength",
        "values": [2, 3, 4, 6, 8]
    },

    "Systematic Bias": {
        "param": "bias_strength",
        "values": [0.2, 0.4,0.3, 0.49]
    },

    "Myopic Decision Policy": {
        "param": "lookback_weeks",
        "values": [1,2, 3,5, 6]
    }
}