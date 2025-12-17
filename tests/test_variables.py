import unittest
import tkinter as tk
from ttkbootstrap.core.variables import SetVar

class TestSetVar(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.destroy()

    def test_setvar_init_empty(self):
        """Test that SetVar initializes with an empty set by default."""
        var = SetVar(master=self.root)
        self.assertEqual(var.get(), set())

    def test_setvar_init_with_value(self):
        """Test that SetVar initializes with a given set value."""
        initial_set = {'a', 'b', 'c'}
        var = SetVar(master=self.root, value=initial_set)
        self.assertEqual(var.get(), initial_set)

    def test_setvar_get(self):
        """Test that get() returns a Python set."""
        initial_set = {'a', 'b'}
        var = SetVar(master=self.root, value=initial_set)
        self.assertIsInstance(var.get(), set)

    def test_setvar_set(self):
        """Test that set() updates the variable's value."""
        var = SetVar(master=self.root)
        new_set = {'x', 'y', 'z'}
        var.set(new_set)
        self.assertEqual(var.get(), new_set)

    def test_setvar_trace(self):
        """Test that a trace callback fires when the variable changes."""
        var = SetVar(master=self.root, value={'a'})
        callback_called = False
        new_value = None

        def trace_callback(*args):
            nonlocal callback_called, new_value
            callback_called = True
            new_value = var.get()

        var.trace_add('write', trace_callback)
        var.set({'b', 'c'})
        self.root.update() # Process events

        self.assertTrue(callback_called)
        self.assertEqual(new_value, {'b', 'c'})

    def test_setvar_empty_set(self):
        """Test that an empty set is handled correctly."""
        var = SetVar(master=self.root, value=set())
        self.assertEqual(var.get(), set())
        var.set({'a'})
        var.set(set())
        self.assertEqual(var.get(), set())

    def test_setvar_single_item(self):
        """Test that a set with a single item is handled correctly."""
        var = SetVar(master=self.root, value={'one'})
        self.assertEqual(var.get(), {'one'})
        var.set({'two'})
        self.assertEqual(var.get(), {'two'})

    def test_setvar_multiple_items(self):
        """Test that a set with multiple items is handled correctly."""
        initial_set = {'one', 'two', 'three'}
        var = SetVar(master=self.root, value=initial_set)
        self.assertEqual(var.get(), initial_set)
        
        new_set = {'four', 'five'}
        var.set(new_set)
        self.assertEqual(var.get(), new_set)

if __name__ == '__main__':
    unittest.main()
