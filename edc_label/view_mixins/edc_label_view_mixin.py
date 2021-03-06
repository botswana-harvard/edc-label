import cups

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import messages
from django.views.generic.base import ContextMixin

from ..printers_mixin import PrintersMixin, PrinterError, PrintServerError

app_config = django_apps.get_app_config('edc_label')


class EdcLabelViewMixin(PrintersMixin, ContextMixin):

    error_messages = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'print_servers': settings.CUPS_SERVERS,
            'selected_print_server_name': self.print_server_name,
            'selected_clinic_label_printer': self.clinic_label_printer,
            'selected_lab_label_printer': self.lab_label_printer,
            'printers': self.printers,
        })
        error_messages = list(set(self.error_messages))
        for message in error_messages:
            messages.error(self.request, message)
        return context

    @property
    def print_server_name(self):
        try:
            print_server_name = super().print_server_name
        except PrintServerError:
            print_server_name = None
        return print_server_name

    @property
    def printers(self):
        try:
            printers = super().printers
        except PrinterError as e:
            printers = None
            self.error_messages.append(str(e))
        except PrintServerError:
            printers = None
        return printers
