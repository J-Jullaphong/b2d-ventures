from django.views.generic import TemplateView


class UnavailableView(TemplateView):
    """View for displaying a custom 404 error page."""
    template_name = "b2d/404.html"

    def get(self, request, *args, **kwargs):
        """Render the custom 404 error page."""
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)
