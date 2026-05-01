
def calculate_gpt_usage_cost(model, in_tokens, out_tokens, n_calls=1):
    # n_calls is to see costs as a function of the number of calls made with this specific query

    # per 1k tokens
    # models must be defined in descending simplicity order
    MODELS = {
        'gpt-4o': {
            'in': 0.005,
            'out': 0.015
        },
        'gpt-4-32k': {
            'in': 0.06,
            'out': 0.12
        },
        'gpt-4': {
            'in': 0.03,
            'out': 0.06
        },
        'gpt-3.5-turbo-0125': {
            'in': 0.0005,
            'out': 0.0015
        },
        'gpt-3.5-turbo-instruct': {
            'in': 0.0015,
            'out': 0.002
        }
    }

    for base_model, info in MODELS.items():
        if model.startswith(base_model):
            model = base_model
            break

    in_cost = (MODELS[model]['in'] / 1000) * in_tokens
    out_cost = (MODELS[model]['out'] / 1000) * out_tokens
    total_cost = in_cost + out_cost

    return in_cost*n_calls, out_cost*n_calls, total_cost*n_calls
