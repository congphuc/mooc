from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

from ars.subjects.models import Subject
from ars.core.views import LoginRequiredMixin
from ars.subjects.models import Enroll
from ars.core.views import BaseView
from ars.reviews.forms import ReviewSubjectForm
from ars.reviews.models import Review

class ListSubjectView(BaseView, ListView):
    model = Subject
    template_name = 'subjects/index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info = {
            'info': {
                'title': 'Subjects List',
                },
            'page_title': 'Subjects List',
        }
        context.update(info)
        return context


class DetailSubjectMixin(object):
    model = Subject
    template_name = 'subjects/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self.request.user.profile, 'student'):
            student = self.request.user.profile.student
            has_reviewed = Review.objects.filter(
                    student=student, subject=self.object).exists()
            if self.object.latest_session is not None:
                has_enrolled = self.object.latest_session.enrolls.filter(student=student).exists()
            else:
                has_enrolled = False
        else:
            has_reviewed = False
            has_enrolled = False
        

        if self.object.latest_session is not None:
            context['num_enrollers'] = self.object.latest_session.enrolls.count()

        info = {
            'info': {
                'title': 'Subject Detail',
                },
            'page_title': 'Subject',
        }
        context.update(info)
        context['has_reviewed'] = has_reviewed
        context['has_enrolled'] = has_enrolled
        return context
    

class DisplaySubjectView(DetailSubjectMixin, BaseView, DetailView):
    pass


class ReviewSubjectView(DetailSubjectMixin, BaseView, SingleObjectMixin, FormView):
    form_class = ReviewSubjectForm
    
    def get_success_url(self):
        return reverse_lazy('subjects:detail', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.profile.is_teacher:
            return HttpResponseForbidden()

        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.request.user.profile.student
        form.instance.subject = self.object
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class DetailSubjectView(View):

    def get(self, request, *args, **kwargs):
        view = DisplaySubjectView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewSubjectView.as_view()
        return view(request, *args, **kwargs)


class EnrollSubjectView(LoginRequiredMixin, CreateView):
    model = Enroll
    fields = ['session']

    def get(self, request, *args, **kwargs):
        return HttpResponse()

    def get_success_url(self):
        return reverse('subjects:detail',
                    kwargs={'pk': self.object.session.subject.pk})
    
    def form_valid(self, form):
        form.instance.student = self.request.user.profile.student
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
