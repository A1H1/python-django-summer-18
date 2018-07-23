from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Avg

from . import models
from . import forms

class SuccessView(TemplateView):
    template_name = "main/success.html"


class IndexView(TemplateView):
    template_name = "main/index.html"


class RestaurantList(ListView):
    model = models.Restaurant
    context_object_name = 'restaurants'
    qs = f = r = None

    def get(self, request, *args, **kwargs):
        self.qs = models.Restaurant.objects.all()
        self.f=request.GET['filter']
        self.r=request.GET['reverse']

        if self.f=='a2z' and self.r=='False':
            self.qs=self.qs.order_by('name')
        elif self.f=='a2z' and self.r=='True':
            self.qs=self.qs.order_by('-name')
        elif self.f=='rating' and self.r=='False':
            self.qs=self.qs.annotate(average_rating=Avg('review__rating')).order_by('average_rating')
        elif self.f=='rating' and self.r=='True':
            self.qs=self.qs.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')
        
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurants'] = self.qs
        context['f'] = self.f            
        context['r'] = self.r
        return context

class RestaurantDetail(DetailView):
    model = models.Restaurant
    context_object_name = 'restaurant'

    def get_context_data(self, object):
        context = super().get_context_data()
        context['form'] =  forms.ReviewForm
        context['success'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ReviewForm(request.POST)
        self.object = self.get_object()
        if form.is_valid():
            obj = form.save(commit = False)
            obj.restaurant = self.object
            obj.save()
            context = super().get_context_data()
            context['form'] = forms.ReviewForm
            context['success'] = True
            return self.render_to_response(context=context)

class RestaurantCreateView(CreateView):
    model = models.Restaurant
    fields = '__all__'
    success_url = '/success/'

class ReviewDetail(DetailView):
    model = models.Review
    context_object_name = 'review'