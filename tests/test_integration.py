from unittest import TestCase

import sublime

from sublime import Region


class TestLinesMultisetsChooseViewCommand(TestCase):

	def setUp(self):
		self.original_window_class = sublime.Window
		sublime.Window = WindowStub

		sublime.run_command('new_window')
		self.window = sublime.active_window()

	def tearDown(self):
		for view in self.window.views():
			view.set_scratch(True)

		self.window.run_command('close_window')

		sublime.Window = self.original_window_class

	def test_execute_specified_operation_on_selected_views(self):
		self.window.new_file()

		empty_view_with_name = self.window.new_file()
		empty_view_with_name.set_name('empty_view_name')

		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': '\n'.join(['line one', 'line two'])})

		active_view = self.window.new_file()
		active_view.run_command('insert', {'characters': '\n'.join(['unique line', 'line one'])})

		active_view.run_command('lines_multisets_choose_view', {'operation_name': 'intersection'})

		new_content = active_view.substr(Region(0, active_view.size()))
		self.assertEqual(new_content, '\n'.join(['line one']))


class WindowStub(sublime.Window):

	def show_quick_panel(self, items, on_select, **_):
		on_select(0 if items else -1)
