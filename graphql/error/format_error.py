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
        # todo: FragmentSpread has no ancestor yet
        while getattr(node, 'ancestor', None):
            node = node.ancestor
            path.insert(0, node)

        try:
            formatted_error['path'] = [getattr(n, 'alias', getattr(n, 'name')).value for n in  path]
        except AttributeError:
            pass


    return formatted_error
