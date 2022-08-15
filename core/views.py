from django.views import generic

class HomeView(generic.TemplateView):
	"""
    Website home page.

    **Template:**

    :template:`core/index.html`
    """
	template_name = "core/index.html"