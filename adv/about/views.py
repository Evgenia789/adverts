from django.views.generic.base import TemplateView


class AboutUsView(TemplateView):
    template_name = 'about/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_title'] = 'О нас'
        context['text'] = 'О нас'
        return context
