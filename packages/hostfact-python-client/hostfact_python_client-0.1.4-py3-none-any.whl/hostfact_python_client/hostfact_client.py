import json
import urllib.request
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)


from hostfact_python_client.utilities import http_build_query


class HostFactCall(object):
    def __init__(self, url, api_key, controller=None, timeout=30, debug=False):
        self.url = url
        self.api_key = api_key
        self.controller = controller
        self.timeout = timeout
        self.debug = debug

    def call(self, **kwargs):
        data={
            "api_key": self.api_key,
            "controller": self.controller,
            "action": self.name,
            **kwargs
        }
        try:
            d = http_build_query(data).encode('ascii')
            with urllib.request.urlopen(self.url, d, timeout=self.timeout) as f:
                reply = f.read()
            reply = json.loads(reply.decode('utf-8'))
        except Exception as e:
            if self.debug:
                error = f"HostFact error: {e}, {e.file.data.decode()}"
                print(error)
            raise Exception(error) from e

        if reply['status'] == 'error':
            if self.debug:
                print(f"HostFact error: {reply}")
            raise Exception(f"HostFact error: {reply['errors']}" if 'errors' in reply.keys() else Exception("HostFact error."))
        return reply

    def make_invoice(self, debtor_code, invoice_lines, newInvoice=False, attachment=None):
        method = HostFactCall(self.url, self.api_key, 'invoice', self.debug)

        active_invoices = []

        if not newInvoice:
            active_invoices = method.list(searchat="DebtorCode", searchfor=debtor_code, status=0, sort="Modified")

        if newInvoice or (not newInvoice and active_invoices['totalresults'] == 0):
            invoice_reply = method.add(DebtorCode=debtor_code, InvoiceLines=invoice_lines)
        else:
            invoice_line_method = HostFactCall(self.url, self.api_key, 'invoiceline', self.debug)
            invoice_reply = invoice_line_method.add(Identifier=active_invoices['invoices'][0]['Identifier'], InvoiceLines=invoice_lines)

        if attachment:
            attachment_method = HostFactCall(self.url, self.api_key, 'attachment', self.debug)
            attachment_method.add(InvoiceCode=invoice_reply['invoice']['InvoiceCode'], Type='invoice', Filename=attachment['name'], Base64=attachment['content'])

        return {"Identifier": invoice_reply['invoice']['Identifier']}

    def __getattr__(self, name):
        if name == "make_invoice":
            if self.controller == "invoice":
                return self.make_invoice
            else:
                raise Exception("make_invoice only allowed for 'invoice' controller")
        self.name = name
        return self.call


class HostFact(object):
    def __init__(self, url, api_key, debug=False):      
        self.url = url
        self.api_key = api_key
        self.method = HostFactCall(self.url, self.api_key, debug=debug)

    def __getattr__(self, name):
        setattr(self.method, "controller", name)
        return self.method
