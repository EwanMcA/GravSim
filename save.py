import stellar

class Save():
    """Class to control saving and resetting the simulation state"""

    def __init__(self, stellarList):
        """Given a list of the current simulation objects, store a list
        of clones of these objects in an instance variable.

        Constructor: Save(list(stellar))

        """

        _saveArray = []
        for stellar in stellarList:
            _saveArray.append(stellar.clone())
    
        self._current_save = _saveArray

    def reset(self):
        """If the state has previously been saved, return a list
        of the objects in the save variable. Then rebuild the save
        variable using clones once more (so that the save state remains
        decoupled from the running simulation.)
        If the state has never been saved, return an empty list.

        reset() -> list(stellar)

        """

        _resetArray = []
        for stellar in self._current_save:
            _resetArray.append(stellar)

        _saveArray = []
        for stellar in self._current_save:
            _saveArray.append(stellar.clone())
        self._current_save = _saveArray

        return _resetArray
