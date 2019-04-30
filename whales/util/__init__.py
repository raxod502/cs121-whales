"""
General utility module.
"""


class UnsetClass:
    """
    Singleton class used to implement `Unset`.
    """

    def __repr__(self):
        return "<Unset>"


# Singleton object that can be used to indicate "no data available".
Unset = UnsetClass()
