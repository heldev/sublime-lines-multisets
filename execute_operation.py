from collections import Counter
import operator

from sublime import Region
from sublime_plugin import TextCommand


OPERATIONS = {
	'sum': operator.add,
	'union': operator.or_,
	'intersection': operator.and_,
	'difference': operator.sub,
	'symmetric_difference': lambda a, b: (a | b) - (a & b)}


class LinesMultisetsOperationCommand(TextCommand):

	def run(self, edit, other_view_id, operation_name):
		operation = OPERATIONS[operation_name]

		current_lines = self.current_line_multiset()
		other_lines = self.line_multiset(other_view_id)

		result_text = self.apply_operation(operation, current_lines, other_lines)

		self.display_result(edit, result_text)

	def current_line_multiset(self):
		self.view.set_status('lines_multisets', 'Loading multiset 1')

		return lines(self.view)

	def line_multiset(self, view_id):
		self.view.set_status('lines_multisets', 'Loading multiset 2')
		view = self.find_view(view_id)

		return lines(view)

	def find_view(self, view_id):
		all_views = self.view.window().views()

		return next(filter(lambda view: view.id() == view_id, all_views))

	def apply_operation(self, operation, multiset1, multiset2):
		self.view.set_status('lines_multisets', 'Calculating results')
		result_lines = sorted(operation(multiset1, multiset2).elements())

		return '\n'.join(result_lines)

	def display_result(self, edit, result_text):
		self.view.set_status('lines_multisets', 'Rendering results')
		self.view.replace(edit, max_region(self.view), result_text)
		self.view.erase_status('lines_multisets')


def lines(view):
	return Counter(view.substr(max_region(view)).splitlines())


def max_region(view):
	return Region(0, view.size())
