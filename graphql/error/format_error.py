def format_error(error):
    formatted_error = {
        'message': error.message,
    }
    if error.locations is not None:
        formatted_error['locations'] = [
            {'line': loc.line, 'column': loc.column}
            for loc in error.locations
        ]

    if error.nodes:
        node = error.nodes[0]
        path = [node]
        while node.ancestor:
            node = node.ancestor
            path.insert(0, node)

        formatted_error['path'] = [(n.alias or n.name).value for n in path]

    return formatted_error
