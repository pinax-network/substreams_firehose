"""
SPDX-License-Identifier: MIT

Generic forms used as base class for other widget-holding forms.
"""

import logging
from collections.abc import Callable, MutableMapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Type

from npyscreen import ActionFormV2, MiniButtonPress, OptionList, SplitForm
from npyscreen import notify_confirm

from pyfirehose.config.ui.widgets.custom import CategorizedItemViewerBoxTitle
from pyfirehose.config.ui.widgets.inputs import InputGeneric, InputListDisplay

class ActionFormDiscard(ActionFormV2):
    """
    Generic class for an action form with an additional *Discard* button.

    Overload the `on_discard` method to customize its behavior.
    """
    class Discard_Button(MiniButtonPress): #pylint: disable=invalid-name
        """
        Additional *Discard* button (name style chosen to match the `npyscreen` library).
        """
        def whenPressed(self):
            self.parent._on_discard() #pylint: disable=protected-access

    DISCARDBUTTON_TYPE = Discard_Button
    DISCARD_BUTTON_BR_OFFSET = (
        ActionFormV2.CANCEL_BUTTON_BR_OFFSET[0],
        ActionFormV2.OK_BUTTON_BR_OFFSET[1]
        + len(ActionFormV2.OK_BUTTON_TEXT)
        + ActionFormV2.CANCEL_BUTTON_BR_OFFSET[1]
        + len(ActionFormV2.CANCEL_BUTTON_TEXT)
    )
    DISCARD_BUTTON_TEXT = 'Discard'

    def _on_discard(self):
        self.editing = self.on_discard()

    def create_control_buttons(self):
        self._add_button('ok_button',
            self.__class__.OKBUTTON_TYPE,
            self.__class__.OK_BUTTON_TEXT,
            0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
            0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
            None
        )

        self._add_button('cancel_button',
            self.__class__.CANCELBUTTON_TYPE,
            self.__class__.CANCEL_BUTTON_TEXT,
            0 - self.__class__.CANCEL_BUTTON_BR_OFFSET[0],
            0 - self.__class__.CANCEL_BUTTON_BR_OFFSET[1] - len(self.__class__.CANCEL_BUTTON_TEXT),
            None
        )

        self._add_button('discard_button',
            self.__class__.DISCARDBUTTON_TYPE,
            self.__class__.DISCARD_BUTTON_TEXT,
            0 - self.__class__.DISCARD_BUTTON_BR_OFFSET[0],
            0 - self.__class__.DISCARD_BUTTON_BR_OFFSET[1] - len(self.__class__.DISCARD_BUTTON_TEXT),
            None
        )

    def on_discard(self) -> bool:
        """
        *Discard* button hook to overload for customizing the behavior of the button.

        Returns:
            A boolean to stop (`False`) or continue (`True`) editing the current form.
        """
        return False

# TODO: Test genericity of class with other `MutableSequence` and items
class CategorizedItemDisplayForm(ActionFormDiscard): #pylint: disable=too-many-instance-attributes
    """
    Display a list of items identified by a unique identifer, grouped by categories.

    Selecting an item will bring up an `ActionButtonPopup` menu to edit or delete the item.
    New items can be added using the third `ActionForm` button at the bottom (`New`).

    Attributes:
        items: A container of items to display. Items must have *gettable* attributes.
        item_fields: A list of `ItemField` describing the fields of an item for edition.
        identifier_key: An attribute of an item uniquely identifying this item from the others. This value will also be used for display.
        category_key: An attribute items share for grouping them by category (set of unique values of that attribute).
        default_category: The default category for items that don't have the `category_key` attribute.
        sort_categories: An optional function used to sort categories (alphabetical by default).
    """
    @dataclass
    class ItemField:
        """
        Local class to store an item field values.

        Attributes:
            name: The field name.
            input_class: The input class from `inputs.py` to use for editing the field.
            input_args: A dictionary with additional arguments to the `input_class`.
            required: A boolean setting the field as required or optional.
            documentation: A list of strings describing the field purpose.
        """
        name: str
        input_class: Type[InputGeneric]
        input_args: dict = field(default_factory=dict)
        required: bool = False
        documentation: list[str] = field(default_factory=list)

    class _CategorizedItemEditForm(ActionFormV2):
        """
        Edit an item fields.

        Fields are marked as required (won't allow empty values) or optional, with different display (color and symbol) for each.
        """
        REQUIRED_FIELD_COLOR = 'WARNING'
        OPTIONAL_FIELD_COLOR = 'GOOD'

        # Using string type hinting to allow forward declarations
        def __init__(self, *args,
            item: MutableMapping,
            item_fields: Sequence['CategorizedItemDisplayForm.ItemField'],
            parent: 'CategorizedItemDisplayForm',
            **kwargs
        ):
            self._item = item
            self._item_fields = item_fields
            self._items_form = parent
            super().__init__(*args, **kwargs)

        def create(self):
            options = OptionList().options
            for item_field in self._item_fields:
                input_color = self.REQUIRED_FIELD_COLOR if item_field.required else self.OPTIONAL_FIELD_COLOR

                options.append(item_field.input_class(
                    name=item_field.name,
                    value=self._item.get(item_field.name, ''),
                    documentation=\
                        [f'{"="*16}', f'=== {"REQUIRED" if item_field.required else "OPTIONAL"} ===', f'{"="*16}'] + item_field.documentation,
                    # Set the color inside the option editing window to match the displayed color from the fields list
                    option_widget_keywords={'labelColor': input_color},
                    **item_field.input_args
                ))

                # Additional `Option` object parameters for display
                options[-1].annotation_color = input_color
                options[-1].required = item_field.required

            self.w_inputs = self.add(
                InputListDisplay,
                w_id='inputs',
                # TODO: Add name describing item types as help text ?
                name='Edit item attributes',
                values=options,
                scroll_exit=True
            )

        def on_ok(self):
            previous_id = self._item.get(self._items_form.identifier_key)

            for item_field in self.w_inputs.values:
                if item_field.required and not item_field.value:
                    notify_confirm(f'A value is required for "{item_field.name}"', title='Error: no value set for required field')
                    return

                # Flag duplicate ids only when renaming
                if item_field.name == self._items_form.identifier_key \
                and item_field.value != previous_id \
                and not self._items_form.is_unique(item_field.value):
                    notify_confirm(
                        f'The "{item_field.value}" id already exists. Please choose another identifier.',
                        title='Error: identifier not unique'
                    )
                    return

                # Get the value from single choice widgets (stored internally as a list in the widget)
                try:
                    item_field.value = item_field.value.pop()
                except (AttributeError, IndexError):
                    pass

                # Check if not empty or a boolean
                is_empty_input = not (item_field.value or isinstance(item_field.value, bool))

                # Delete any previously set parameter if it's empty or ignore it.
                if item_field.name in self._item and is_empty_input:
                    del self._item[item_field.name]
                elif not is_empty_input:
                    self._item[item_field.name] = item_field.value

            # Update the items list display to move the edited item to its new corresponding `BoxTitle`
            self._items_form.move_to_boxtitle(self._item)
            self._items_form.select_item(self._item)

            self.parentApp.setNextFormPrevious()

        def on_cancel(self):
            self.parentApp.setNextFormPrevious()

    DISCARD_BUTTON_TEXT = 'New'
    # Needed so that `self.editw` (controlling the focused widget in the form) doesn't get reset when starting to edit the form
    PRESERVE_SELECTED_WIDGET_DEFAULT = True

    def __init__(self, *args,
        items: Sequence[MutableMapping],
        item_fields: Sequence[ItemField],
        identifier_key: Any,
        category_key: Any,
        default_category: str = 'Unknown',
        sort_categories: Callable[[set[str]], set[str]] | None = sorted,
        **kwargs
    ):
        self.items = items
        self.item_fields = item_fields
        self.identifier_key = identifier_key
        self.category_key = category_key
        self.default_category = default_category
        self.sort_categories = sort_categories
        super().__init__(*args, **kwargs)

    def create(self):
        self.w_items_boxtitle = []

        # Create a `BoxTitle` widget for each unique values of the `category` attribute
        categories = self.sort_categories({entry.get(self.category_key, self.default_category) for entry in self.items})
        n_items = len(categories)
        for category in categories:
            self.w_items_boxtitle.append(self.add(
                CategorizedItemViewerBoxTitle,
                name=category,
                values=[entry for entry in self.items if entry.get(self.category_key, self.default_category) == category],
                max_height=self.lines//n_items - 4,
                scroll_exit=True,
            ))

    def create_item_edit_form(self, item: MutableMapping) -> None:
        """
        Create and start a `_CategorizedItemEditForm` for editing the specified item.

        Args:
            item: The current state of the item.
        """
        self.parentApp.addForm(
            self.parentApp.CATEGORIZED_ITEM_EDIT_FORM,
            self._CategorizedItemEditForm,
            # TODO: Add name describing item types as help text ?
            name='Main config editing - Edit item',
            item=item,
            item_fields=self.item_fields,
            parent=self
        )
        self.parentApp.switchForm(self.parentApp.CATEGORIZED_ITEM_EDIT_FORM)

    def display(self, clear: bool = True) -> None:
        """
        Overwrite `display` method to prevent widget showing blank after returning from the help message display.

        See [`h_display_help()`](
            https://github.com/npcole/npyscreen/blob/8ce31204e1de1fbd2939ffe2d8c3b3120e93a4d0/build/lib/npyscreen/fmForm.py#L208
        ) in `npyscreen` code for reference.
        """
        super().display(clear)

    def on_ok(self) -> list[MutableMapping]:
        """
        Hook for the `OK` button to return all the updated item values.

        This can be used in overloaded methods to perform additional checks, transforms or store the updated data.

        Returns:
            The list of updated items.
        """
        new_items = []
        for boxtitle in self.w_items_boxtitle:
            new_items.extend(boxtitle.values)

        self.parentApp.setNextFormPrevious()
        return new_items

    def on_cancel(self):
        # self.parentApp.restore_main_config_backup()
        self.parentApp.setNextFormPrevious()

    def on_discard(self) -> bool:
        """
        Override the default 'discard' behavior to create an new item entry.
        """
        self.create_item_edit_form(type(next(iter(self.items), None))())
        return False

    def is_unique(self, item_id: Any) -> bool:
        """
        Check that the item identified by the `item_id` is not already present in the displayed values.

        Args:
            item_id: An identifier unique to each item.

        Returns:
            A boolean indicating if the identifier is already present.

        Raises:
            ValueError: If the `item_id` is `None`.
        """
        if item_id is None:
            raise ValueError('Item id cannot be `None`')

        return item_id not in [v.get(self.identifier_key) for w in self.w_items_boxtitle for v in w.values]

    def move_to_boxtitle(self, item: MutableMapping) -> None:
        """
        Remove the specified item from its previous `BoxTitle` and add it to the new one defined in its category attribute.

        Args:
            item: The item to move.
        """
        for boxtitle_widget in self.w_items_boxtitle:
            # Try to remove the item first
            boxtitle_widget.values = [v for v in boxtitle_widget.values if v.get(self.identifier_key) != item.get(self.identifier_key)]

            # Add it to the appropriate category
            if item.get(self.category_key, self.default_category) == boxtitle_widget.name:
                boxtitle_widget.values.append(item)

    def select_item(self, item: MutableMapping) -> None:
        """
        Move the cursor to the specified item in the form. Used when editing is finished to select the edited item.

        Args:
            item: The item to select.
        """
        for boxtitle_widget in self.w_items_boxtitle:
            if item.get(self.category_key, self.default_category) == boxtitle_widget.name:
                try:
                    # Update cursor position within the `BoxTitle` widget
                    boxtitle_widget.entry_widget.cursor_line = boxtitle_widget.values.index(item)

                    # Update the focused `BoxTitle` widget within the form
                    self.editw = self.w_items_boxtitle.index(boxtitle_widget) #pylint: disable=attribute-defined-outside-init
                except ValueError:
                    logging.error('[%s] Item not found in %s widget : %s', self.name, boxtitle_widget.name, item)
                    raise

class SplitActionForm(ActionFormV2, SplitForm): #pylint: disable=too-many-ancestors
    """
    Combine `ActionFormV2` buttons with `SplitForm` horizontal line display.

    Attributes:
        draw_line_at: An integer y-coordinate of the horizontal line splitting the screen (half-screen by defaut).
    """
    def get_half_way(self, draw_line_at: int | None = None) -> int:
        if not hasattr(self, 'draw_line_at'):
            self.draw_line_at = draw_line_at if draw_line_at else self.curses_pad.getmaxyx()[0] // 2

        return self.draw_line_at
