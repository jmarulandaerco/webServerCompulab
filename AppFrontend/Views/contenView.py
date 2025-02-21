from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
from django.views.generic import TemplateView
from django.conf import settings

class ContentView(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = f'home/content/{option}.html'

        try:
            return render(request, template_name)
        except:
            return HttpResponse(f"<h1>{option} - Página en construcción</h1>")
        

class ContentViewMenuMain(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = f'home/content/form/main/{option}.html'
        try:
            return render(request, template_name)
        except Exception as e:
            print(e)
            
            return HttpResponse(f"<h1>{option} - Página en construcción</h1>")
        

class ContentViewMenuModbus(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = f'home/content/form/modbus/{option}.html'
        try:
            return render(request, template_name)
        except Exception as e:
            print(e)
            
            return HttpResponse(f"<h1>{option} - Página en construcción</h1>")
        
class ContentViewMenuCompensationLimitation(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = f'home/content/form/compensation_limitatation/{option}.html'
        try:
            return render(request, template_name)
        except Exception as e:
            print(e)
            
            return HttpResponse(f"<h1>{option} - Página en construcción</h1>")
        
class ContentViewMenuDatabase(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = f'home/content/form/database/{option}.html'
        try:
            return render(request, template_name)
        except Exception as e:
            print(e)
            
            return HttpResponse(f"<h1>{option} - Página en construcción</h1>")
        
class ContentViewMenuChecker(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = f'home/content/form/checker/{option}.html'
        try:
            return render(request, template_name)
        except Exception as e:
            print(e)
            
            return HttpResponse(f"<h1>{option} - Página en construcción</h1>")
        
class ContentViewMenuSetting(TemplateView):

    def get(self, request, *args, **kwargs):
        if 'option' in kwargs:
            return self.get_content(request, kwargs['option'])
        return super().get(request, *args, **kwargs)

    def get_content(self, request, option):
        template_name = f'home/content/form/setting/{option}.html'
        try:
            return render(request, template_name)
        except Exception as e:
            print(e)
            
            return HttpResponse(f"<h1>{option} - Página en construcción</h1>")
        
