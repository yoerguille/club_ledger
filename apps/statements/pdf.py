from django.template.loader import render_to_string
from weasyprint import HTML


class PdfRenderer:

    template_name = "statements/statement_detail.html"

    def render(self, context, base_url):

        html = render_to_string(
            self.template_name,
            context,
        )

        return HTML(
            string=html,
            base_url=base_url
        ).write_pdf()