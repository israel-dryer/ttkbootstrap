import unittest
import tkinter as tk
from ttkbootstrap.widgets.composites.togglegroup import ToggleGroup
from ttkbootstrap.core.variables import SetVar
from ttkbootstrap.core.signals import Signal

class TestToggleGroup(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.destroy()

    # 1. Initialization Tests
    def test_init_single_mode_with_stringvar(self):
        var = tk.StringVar()
        group = ToggleGroup(self.root, mode='single', variable=var)
        self.assertIs(group.variable, var)

    def test_init_single_mode_with_signal(self):
        sig = Signal("a")
        group = ToggleGroup(self.root, mode='single', signal=sig)
        self.assertIs(group.signal, sig)
        self.assertEqual(group.get(), "a")

    def test_init_multi_mode_with_setvar(self):
        var = SetVar()
        group = ToggleGroup(self.root, mode='multi', variable=var)
        self.assertIs(group.variable, var)

    def test_init_multi_mode_with_signal(self):
        sig = Signal({'a', 'b'})
        group = ToggleGroup(self.root, mode='multi', signal=sig)
        self.assertIs(group.signal, sig)
        self.assertEqual(group.get(), {'a', 'b'})

    def test_init_with_initial_value(self):
        group_single = ToggleGroup(self.root, mode='single', value='b')
        group_single.add(text='A', value='a')
        group_single.add(text='B', value='b')
        self.assertEqual(group_single.get(), 'b')

        group_multi = ToggleGroup(self.root, mode='multi', value={'b', 'c'})
        group_multi.add(text='A', value='a')
        group_multi.add(text='B', value='b')
        group_multi.add(text='C', value='c')
        self.assertEqual(group_multi.get(), {'b', 'c'})

    # 2. Button Management Tests
    def test_add_and_get_buttons(self):
        group = ToggleGroup(self.root)
        btn1 = group.add(text='A', value='a')
        btn2 = group.add(text='B', value='b')
        self.assertEqual(len(group.buttons()), 2)
        self.assertIs(group.get_button('a'), btn1)
        self.assertIs(group.get_button('b'), btn2)

    def test_remove_button(self):
        group = ToggleGroup(self.root)
        group.add(text='A', value='a')
        group.add(text='B', value='b')
        group.remove('a')
        self.assertEqual(len(group.buttons()), 1)
        with self.assertRaises(KeyError):
            group.get_button('a')

    def test_clear_buttons(self):
        group = ToggleGroup(self.root)
        group.add(text='A', value='a')
        group.add(text='B', value='b')
        group.clear()
        self.assertEqual(len(group.buttons()), 0)

    # 3. Value Handling Tests
    def test_get_set_single_mode(self):
        group = ToggleGroup(self.root, mode='single')
        group.add(text='A', value='a')
        group.add(text='B', value='b')
        group.set('b')
        self.assertEqual(group.get(), 'b')

    def test_get_set_multi_mode(self):
        group = ToggleGroup(self.root, mode='multi')
        group.add(text='A', value='a')
        group.add(text='B', value='b')
        group.set({'a', 'b'})
        self.assertEqual(group.get(), {'a', 'b'})

    def test_variable_sync_single_mode(self):
        var = tk.StringVar(value='a')
        group = ToggleGroup(self.root, mode='single', variable=var)
        group.add(text='A', value='a')
        b_button = group.add(text='B', value='b')
        
        # Test variable -> widget
        var.set('b')
        self.assertEqual(group.get(), 'b')
        
        # Test widget -> variable
        b_button.invoke()
        self.assertEqual(var.get(), 'b') # Should still be b as it's a radio

        a_button = group.get_button('a')
        a_button.invoke()
        self.assertEqual(var.get(), 'a')

    def test_variable_sync_multi_mode(self):
        var = SetVar(value={'a'})
        group = ToggleGroup(self.root, mode='multi', variable=var)
        group.add(text='A', value='a')
        b_button = group.add(text='B', value='b')

        # Test variable -> widget
        var.set({'b'})
        self.assertEqual(group.get(), {'b'})

        # Test widget -> variable
        b_button.invoke() # 'b' is already in set, so this should remove it
        self.assertEqual(var.get(), set())
        b_button.invoke() # Add 'b' back
        self.assertEqual(var.get(), {'b'})

    def test_signal_sync(self):
        sig = Signal("a")
        group = ToggleGroup(self.root, mode='single', signal=sig)
        group.add(text='A', value='a')
        group.add(text='B', value='b')
        
        # Test signal -> widget
        sig.set("b")
        self.assertEqual(group.get(), "b")

        # Test widget -> signal
        group.get_button('a').invoke()
        self.assertEqual(sig.get(), "a")

    # 4. UI Layout Tests
    def test_orientation(self):
        h_group = ToggleGroup(self.root, orientation='horizontal')
        h_btn = h_group.add(value='a')
        self.assertEqual(h_btn.pack_info()['side'], 'left')

        v_group = ToggleGroup(self.root, orientation='vertical')
        v_btn = v_group.add(value='a')
        self.assertEqual(v_btn.pack_info()['side'], 'top')

    def test_bootstyle_propagation(self):
        group = ToggleGroup(self.root, bootstyle='danger')
        button = group.add(value='a')
        self.assertIn('danger', button.cget('bootstyle'))

if __name__ == '__main__':
    unittest.main()
