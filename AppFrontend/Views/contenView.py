from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

class BaseContentView(TemplateView):
    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = self.get_template_name(option)
        try:
            return render(request, template_name)
        except Exception as e:
            print(e)
            return HttpResponse(f"<h1>{option} - Error loading page</h1>")

    def get_template_name(self, option):
        """
        Método abstracto que debe ser implementado por las subclases
        para definir la ruta de la plantilla correspondiente.
        """
        raise NotImplementedError("Subclases deben implementar este método.")
class ContentView(BaseContentView):
    def get_template_name(self, option):
        return f'home/content/{option}.html'

class ContentViewMenuMain(BaseContentView):
    def get_template_name(self, option):
        return f'home/content/form/main/{option}.html'

class ContentViewMenuModbus(BaseContentView):
    def get_template_name(self, option):
        return f'home/content/form/modbus/{option}.html'

class ContentViewMenuCompensationLimitation(BaseContentView):
    def get_template_name(self, option):
        return f'home/content/form/compensation_limitatation/{option}.html'

class ContentViewMenuDatabase(BaseContentView):
    def get_template_name(self, option):
        return f'home/content/form/database/{option}.html'

class ContentViewMenuChecker(BaseContentView):
    def get_template_name(self, option):
        return f'home/content/form/checker/{option}.html'

class ContentViewMenuSetting(BaseContentView):
    def get_template_name(self, option):
        return f'home/content/form/setting/{option}.html'
