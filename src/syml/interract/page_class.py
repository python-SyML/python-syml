from abc import ABC
from abc import abstractmethod

import streamlit as st


class BasePageElement(ABC):
    def __init__(self):
        self.actions = [self.introduction]
        self.children = {}
        self.setup()

    def setup_child(self, child):
        """Use this method to add a child element to the current page. That way, the actions of the child instance
        are automatically added to the actions list of the parent instance."""

        self.children[child.name] = child
        self.actions.append(st.divider)
        self.actions += child.actions

    def display(self):
        for action in self.actions:
            action()

    @abstractmethod
    def introduction(self):
        """Display the introduction paragraph."""

    @abstractmethod
    def setup(self):
        """Setup the class instance with its actions and children."""
