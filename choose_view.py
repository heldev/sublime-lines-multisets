from functools import partial

from sublime import Region
from sublime_plugin import TextCommand


class LinesMultisetsChooseViewCommand(TextCommand):

	def run(self, _, operation_name):
		titles = tuple(map(title, self.other_views))

		self.view.window().show_quick_panel(titles, partial(self.run_operation, operation_name))

	def run_operation(self, operation_name, other_view_index):
		if other_view_index >= 0:
			other_view_id = self.other_views[other_view_index].id()
			operation_arguments = {'other_view_id': other_view_id, 'operation_name': operation_name}
			self.view.run_command('lines_multisets_operation', operation_arguments)

	@property
	def other_views(self):
		all_views = self.view.window().views()

		return tuple(filter(self.is_other_view_with_content, all_views))

	def is_other_view_with_content(self, view):
		return view.id() != self.view.id() and content_preview(view)


def title(view):

	return view.name() \
			or view.file_name() \
			or '"{}"'.format(content_preview(view))


def content_preview(view):
	return view.substr(Region(0, 1024)).strip()
