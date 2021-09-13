from io import BytesIO

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template


from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)

    context=context_dict
    html  = template.render(context)
    result = BytesIO()

    #This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
