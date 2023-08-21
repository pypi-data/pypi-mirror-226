"""
admin page decorators module.
"""


def link(method):
    """
    decorator to flag an admin method as rendering a link on client list view.

    :param object method: method to be flagged.

    :returns: method.
    :rtype: type
    """

    setattr(method, 'is_link', True)
    return method


def action(method):
    """
    decorator to flag an admin method as rendering an action button on client list view.

    :param object method: method to be flagged.

    :returns: method.
    :rtype: type
    """

    setattr(method, 'is_action', True)
    return method
