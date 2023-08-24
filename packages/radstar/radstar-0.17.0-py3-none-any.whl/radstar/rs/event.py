# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC


class Event:
    def __init__(self):
        self._handlers = []

    def emit(self, *args, **kw):
        for x in self._handlers:
            x(*args, **kw)

    def __call__(self, func):
        self._handlers.append(func)
