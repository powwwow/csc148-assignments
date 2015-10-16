"""Assignment 1 - Grocery Store Events (Task 2)

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
# Feel free to import classes and functions from
# *your other files*, but remember not to import any external libraries.


class Event:
    """An event.

    Events have an ordering based on the event timestamp in non-ascending
    order. Events with older timestamps are less than those with newer
    timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """
    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return whether this Event is equal to <other>.

        Two events are equal if they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self.__le__(other)

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self.__lt__(other)

    def distribute_info(self, name, item_num, time_waited, checkout_line):
        """places important info into the event object

        @type name: str
        @type item_num: int
        @type time_waited: int
        @type checkout_line: int
        """
        self.name = name
        self.item_carried = item_num
        self.time_waited = time_waited
        self.line = checkout_line

    def do(self, store):
        """Perform this Event.

        Call methods on <store> to update its state according to the
        meaning of the event. Note: the "business logic" of what actually
        happens inside a grocery store should be handled in the GroceryStore
        class, not in any Event classes.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        @type self: Event
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        raise NotImplementedError


# TODO: Create subclasses for the different types of events below.

class New_Customer(Event):
    """ Subclass of event

    Handles the event where a new customer arrives and is ready
    to be taken to a line

    """
    def do (self, store):
        """Over riding the do method from super class

        @type store: GroceryStore
        @rtype: tuple(event, str)
            returns a checkout_begins event
        """
        return (store.new_customer(self), 'one event')

class Checkout_Begins(Event):
    """Subclass of event

    Handles the event when customers begin check out
    """

    def do (self, store):
        """basically same as do method for New_Customer

        @type store: GroceryStore
        @rtype: tuple(Event, str)
            returns a checkout_finish event
        """
        return (store.checkout_begins(self), 'one event')

class Checkout_Finish(Event):
    """Subclass of event

    Handles the event in which customer finishes checkout
    next customer is given new checkout begins event
    and time advances
    """

    def do (self, store):
        """similar method as the do for the other sub classes

        @type store: GroceryStore
        @rtype: tuple(int, str)
            returns the total wait time for
            for this customer checkout
        """
        return (store.checkout_finish(self), 'int')

class Line_Close(Event):
    """ Subclass of event

    Handles the event where a line is closed
    Customers in the line must be redistributed to other lines

    """
    def line_setup(self, index):
        self.line_index = index

    def do (self, store):
        """do method of line closing event

        when lines close, all remaining customers in the line will
        be transformed into new_customer events while maintianing
        their time_waited

        @type store: GroceryStore
        @rtype: tuple(list[Event], str)
            this list of events contain the the new customer events in order
            which is from last to first, with one second intervals
        """

        return (store.line_close(self), 'event list')

# TODO: Complete this function, which creates a list of events from a file.
def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    events.append(0) #counting number of customers
    new_event = 0
    with open(filename, 'r') as file:
        for line in file:
            # Create a list of words in the line, e.g.
            # ['60', 'Arrive', 'Bob', '5'].
            # Note that these are strings, and you'll need to convert some of
            # them to ints.
            tokens = line.split()
            if len(tokens) == 4:
                events[0] += 1
                new_event = New_Customer(tokens[0])
                new_event.distribute_info(tokens[2], int(tokens[3]), 0, -1)
            elif len(tokens) == 3:
                new_event = Line_Close(tokens[0])
                new_event.line_setup(int(tokens[2]))
            events.append(new_event)

    return events


if __name__ == '__main__':
    import doctest
    doctest.testmod()
