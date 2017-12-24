from unittest import TestCase

import sublime

from sublime import Region


class TestLinesMultisetsChooseViewCommand(TestCase):

	def setUp(self):
		sublime.run_command('new_window')
		self.window = sublime.active_window()

	def tearDown(self):
		for view in self.window.views():
			view.set_scratch(True)

		self.window.run_command('close_window')

	def test_populates_current_view_with_all_lines_from_both_views(self):
		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': '\n'.join(['1', '2', '3', '3'])})

		active_view = self.window.new_file()
		active_view.run_command('insert', {'characters': '\n'.join(['0', '2', '3'])})

		operation = {'other_view_id': other_view.id(), 'operation_name': 'sum'}
		active_view.run_command('lines_multisets_operation', operation)

		new_content = active_view.substr(Region(0, active_view.size()))
		self.assertEqual(new_content.splitlines(), ['0', '1', '2', '2', '3', '3', '3'])

	def test_populates_current_view_with_union_of_views(self):
		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': '\n'.join(['1', '2', '3', '3'])})

		active_view = self.window.new_file()
		active_view.run_command('insert', {'characters': '\n'.join(['0', '2', '3'])})

		operation = {'other_view_id': other_view.id(), 'operation_name': 'union'}
		active_view.run_command('lines_multisets_operation', operation)

		new_content = active_view.substr(Region(0, active_view.size()))
		self.assertEqual(new_content.splitlines(), ['0', '1', '2', '3', '3'])

	def test_populates_current_view_with_intersection_of_views(self):
		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': '\n'.join(['1', '2', '2', '3', '3', '4'])})

		active_view = self.window.new_file()
		active_view.run_command('insert', {'characters': '\n'.join(['0', '2', '2', '2', '3', '4'])})

		operation = {'other_view_id': other_view.id(), 'operation_name': 'intersection'}
		active_view.run_command('lines_multisets_operation', operation)

		new_content = active_view.substr(Region(0, active_view.size()))
		self.assertEqual(new_content.splitlines(), ['2', '2', '3', '4'])

	def test_populates_current_view_with_symmetric_difference_of_views(self):
		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': '\n'.join(['1', '2', '2', '3', '3', '3', '4'])})

		active_view = self.window.new_file()
		active_view.run_command('insert', {'characters': '\n'.join(['0', '2', '2', '2', '3', '4'])})

		operation = {'other_view_id': other_view.id(), 'operation_name': 'symmetric_difference'}
		active_view.run_command('lines_multisets_operation', operation)

		new_content = active_view.substr(Region(0, active_view.size()))
		self.assertEqual(new_content.splitlines(), ['0', '1', '2', '3', '3'])

	def test_populates_current_view_with_difference_of_views(self):
		other_view = self.window.new_file()
		other_view.run_command('insert', {'characters': '\n'.join(['1', '2', '2', '3', '3', '3', '4', '5'])})

		active_view = self.window.new_file()
		active_view.run_command('insert', {'characters': '\n'.join(['0', '2', '2', '2', '3', '4', '5', '5', '5'])})

		operation = {'other_view_id': other_view.id(), 'operation_name': 'difference'}
		active_view.run_command('lines_multisets_operation', operation)

		new_content = active_view.substr(Region(0, active_view.size()))
		self.assertEqual(new_content.splitlines(), ['0', '2', '5', '5'])
