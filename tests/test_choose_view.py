from unittest import TestCase

import sublime


class TestLinesMultisetsChooseViewCommand(TestCase):

	def setUp(self):
		self.original_window_class = sublime.Window
		sublime.Window = WindowSpy
		self.original_view_class = sublime.View
		sublime.View = ViewStub

		sublime.run_command('new_window')
		self.window = sublime.active_window()

	def tearDown(self):
		ViewStub.reset()
		WindowSpy.reset()

		for view in self.window.views():
			view.set_scratch(True)

		self.window.run_command('close_window')

		sublime.View = self.original_view_class
		sublime.Window = self.original_window_class

	def test_suggest_tab_titles_with_trimmed_content_preview(self):
		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': '  lines\n with spaces  '})

		active_view = self.window.new_file()
		active_view.run_command('lines_multisets_choose_view', {'operation_name': ''})

		self.assertIn('"lines\n   with spaces"', WindowSpy.quick_panel_items)

	def test_prefer_tab_file_name_over_content_preview(self):
		ViewStub.file_name_override = 'unit-test-file.tst'

		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': 'content'})

		active_view = self.window.new_file()
		self.window.focus_view(active_view)
		active_view.run_command('lines_multisets_choose_view', {'operation_name': ''})

		self.assertIn('unit-test-file.tst', WindowSpy.quick_panel_items)

	def test_prefer_tab_name_over_file_name(self):
		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': 'content'})
		other_view.set_name('tab name')

		active_view = self.window.new_file()
		active_view.run_command('lines_multisets_choose_view', {'operation_name': ''})

		self.assertIn('tab name', WindowSpy.quick_panel_items)

	def test_not_show_current_and_empty_views(self):
		other_view = self.window.new_file()
		other_view.set_name('tab name')

		active_view = self.window.new_file()
		active_view.run_command('insert', {'characters': 'current_view_with_content'})
		active_view.run_command('lines_multisets_choose_view', {'operation_name': ''})

		self.assertCountEqual([], WindowSpy.quick_panel_items)


class WindowSpy(sublime.Window):

	quick_panel_items = []

	def show_quick_panel(self, items, on_select, **_):
		type(self).quick_panel_items = items

	@classmethod
	def reset(cls):
		cls.quick_panel_items = []


class ViewStub(sublime.View):

	file_name_override = None

	def file_name(self):
		return type(self).file_name_override or super().file_name()

	@classmethod
	def reset(cls):
		cls.file_name_override = None
