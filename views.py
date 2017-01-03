
from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .forms import MainForm
from .assemble import assemble

SITE_HDR = "Emu86: an x86 assembly emulator."

registers = OrderedDict(
            [
                ('EAX', 0),
                ('EBX', 0),
                ('ECX', 0),
                ('EDX', 0),
                ('ESI', 0),
                ('EDI', 0),
                ('ESP', 0),
                ('EBP', 0),
            ])

hex_digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
                'C', 'D', 'E', 'F' ]

def get_hdr():
    return SITE_HDR

def main(request):
    global registers
    global hex_digits
    output = ""
    error = ""
    debug = ""

    site_hdr = get_hdr()

    if request.method == 'POST':
        form = MainForm(request.POST)
        (output, error, debug) = assemble(request.POST['code'], registers)
    else:
        form = MainForm()

    return render(request, 'main.html',
                  {'form': form, 'header': site_hdr,
                   'registers': registers, 'output': output,
                   'error': error, 'hex_digits': hex_digits,
                   'debug': debug})

def help(request):
    site_hdr = get_hdr()
    return render(request, 'help.html', {'header': site_hdr})


def feedback(request):
    site_hdr = get_hdr()
    email_list = AdminEmail.objects.all()
    comma_del_emails = ""
    for email in email_list:
        comma_del_emails = comma_del_emails + email.email_addr + ","
    comma_del_emails = comma_del_emails[:-1]
    return render(request, 'feedback.html', {'emails': comma_del_emails,
        'header': site_hdr})

def move(code):
    pass

def add(code):
    pass
