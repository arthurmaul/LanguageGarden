def parse_parameters(tokens):
    match tokens[0].symbol:
        case "[":
            generics = extract_until("]", tokens)
            generics_list = [Type(g.symbol) for g in generics]
        case other: generic_list = None
    raw_params = extract_until(")", tokens)
    params = [{"type": "parameter", v.symbol, Type(t.symbol)) for v, t in zip(parameters[::2], parameters[1::2])]
    raw_returns = extract_until("=", tokens)
    returns = [Type(r.symbol) for r in raw_returns]
    body = extract_until("}", tokens)
    if not generics_list:
        return {"method", "params": parameter_list, return_list, body)
    return GenericMethod(generics_list, parameter_list, return_list, body)

def extract_until(closer, tokens):
    elements = list()
    tokens.pop(0)
    while tokens[0].symbol != closer:
        elements.append(tokens.pop(0))
    tokens.pop(0)
    return elements


