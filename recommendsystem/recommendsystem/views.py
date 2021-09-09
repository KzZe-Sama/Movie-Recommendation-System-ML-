from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .script.movie_recommender import MovieRecommender
class FetchMovieView(TemplateView):
    context = {"searched":False}
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        self.context = {}
        self.context = {"searched":False}
        return render(request,template_name=self.template_name,context=self.context)
    def post(self, request, *args, **kwargs):
        try:
            movie_name = (request.POST.get("movie"))
            instance = MovieRecommender()
            result= instance.main(movie_name)
            self.context["results"] = result
            self.context["movie_name"] = movie_name
            self.context["searched"] = True
            return render(request,template_name=self.template_name,context=self.context)
        except Exception as e:
            self.context = {"searched":True}
            return render(request,template_name=self.template_name,context=self.context)
