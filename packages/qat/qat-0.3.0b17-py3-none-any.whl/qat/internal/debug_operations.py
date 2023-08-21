# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Functions used for development and debugging purposes
"""

from qat.internal.application_context import ApplicationContext
from qat.internal.qt_object import QtObject


def activate_picker(app_context: ApplicationContext):
    """
    Activate the object picker
    """
    command = {}
    command['command'] = 'action'
    command['attribute'] = 'picker'
    command['args'] = 'enable'

    return app_context.send_command(command)


def deactivate_picker(app_context: ApplicationContext):
    """
    Deactivate the object picker
    """
    command = {}
    command['command'] = 'action'
    command['attribute'] = 'picker'
    command['args'] = 'disable'

    return app_context.send_command(command)


def pick(
        app_context: ApplicationContext,
        object_def: dict):
    """
    Simulate a picking event for the given object
    """
    if isinstance(object_def, QtObject):
        object_def = object_def.get_definition()
    command = {}
    command['command'] = 'action'
    command['attribute'] = 'picker'
    command['args'] = 'pick'
    command['object'] = object_def

    return app_context.send_command(command)
