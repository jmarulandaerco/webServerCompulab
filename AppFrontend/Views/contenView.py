from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from utils.logger import LoggerHandler

class BaseContentView(TemplateView):
    """
    A base class for rendering content views based on the option provided in the URL.

    This class provides the logic to load a content template dynamically based on an 'option'
    parameter passed in the URL. Subclasses must implement the `get_template_name` method.

    Methods:
    -------
    get(request, *args, **kwargs)
        Handles GET requests and checks for the 'option' parameter to determine which content to render.

    get_content(request, option)
        Renders the template corresponding to the 'option' or returns an error response if the template fails to load.

    get_template_name(option)
        Abstract method that must be implemented by subclasses to define the template name.
    """
    logger = LoggerHandler().get_logger()

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = self.get_template_name(option)
        try:
            return render(request, template_name)
        except Exception as ex:
            
            self.logger.error(f"Error loding page: {ex}")
            return HttpResponse(f"<h1>{option} - Error loading page</h1>")

    def get_template_name(self, option):
        """
      
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
