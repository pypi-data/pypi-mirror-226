from ast import Tuple
from typing import Callable, Union, Any, Set


class Observer():
    """
    Observer class implements the observer pattern for data monitoring and updates.

    Attributes:
        observers (Set[Callable]): A set of callback functions that are interested in data changes.
        data (Any): The monitored data.

    Methods:
        getData() -> Any:
            Returns the current data.

        subscribe(callback: Callable, get_current=False) -> SubscriptionObserver:
            Subscribes the callback to data changes. If `get_current` is True, the callback will be immediately called
            with the current data.

        next(data: Any) -> None:
            Sets the data to the given value and notifies all observers.

        update(update_callback: Callable, *args, **kwargs) -> None:
            Updates the current data using the provided update function and notifies all observers.
    """

    def __init__(self, data: Union[Any, None] = None) -> None:
        """
        Initializes a new instance of Observer class.

        Parameters:
            data (Any, optional): Initial data. Defaults to None.
        """
        self.observers: Set[Callable] = set()
        self.data = data

    def getData(self):
        """Returns the current data."""
        return self.data

    def subscribe(self, callback: Callable, get_current=False):
        """
        Subscribes the callback to data changes.

        Parameters:
            callback (Callable): The function to call when data changes.
            get_current (bool, optional): Whether or not to immediately invoke the callback with the current data.
                                          Defaults to False.

        Returns:
            SubscriptionObserver: A subscription object which can be used to unsubscribe.
        """
        self._validate_callback(callback)
        self.observers.add(callback)
        if get_current:
            try:
                callback(self.data)
            except:
                pass
        return SubscriptionObserver(callback, self.observers)

    def next(self, data: Union[Any, None] = None):
        """
        Sets the data to the given value and notifies all observers.

        Parameters:
            data (Any): New data value.
        """
        for callable in self.observers.copy():
            try:
                callable(data)
            except:
                pass

    def update(self, update_callback: Callable, *args, **kwargs):
        """
        Updates the current data using the provided update function and notifies all observers.

        Parameters:
            update_callback (Callable): The function that produces the new data value.
            *args: Variable length argument list for the `update_callback`.
            **kwargs: Arbitrary keyword arguments for the `update_callback`.
        """
        self.data = update_callback(self.data, *args, **kwargs)
        self.next(self.data)

    def _validate_callback(self, callback: Callable):
        if not callback:
            raise ObserverError("Callable is required")


class ObserverError(Exception):
    def __init__(self, message: str = "ObserverError error"):
        super().__init__(message)

    def __str__(self):
        original_message = super().__str__()
        return f"ObserverError error: {original_message}"


class SubscriptionObserver():
    """
    SubscriptionObserver class provides a way to manage subscriptions in the Observer pattern.

    Attributes:
        handlers (Set[Callable]): A set of callback functions that the Subscription is managing.
        callback (Callable): The specific callback function for this subscription.

    Methods:
        unsubscribe() -> None:
            Removes the callback from the set of handlers. This effectively unsubscribes from data changes.
    """
    def __init__(self, callback: Callable, handlers: Set[Callable]):
        self.handlers: Set = handlers
        self.callback: Callable = callback

    def unsubscribe(self):
        if self.callback in self.handlers:
            self.handlers.remove(self.callback)
        else:
            raise ObserverError(
                f"There is not callback subscribed")
