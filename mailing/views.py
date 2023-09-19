from random import sample
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from blog.models import BlogPost
from .models import Mailing, Client, Message, Log
from .forms import MailingForm, MessageForm, ClientForm


class HomeView(TemplateView):
    template_name = 'mailing/home.html'
    extra_context = {
        'title': 'Главная страница',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_posts = list(BlogPost.objects.all())
        context['random_blog_posts'] = sample(all_posts, min(3, len(all_posts)))
        context['object_list'] = Mailing.objects.all()
        user = self.request.user
        user_group_names = [group.name for group in user.groups.all()]
        context['user_group_names'] = user_group_names
        return context


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/create_mailing.html'

    def form_valid(self, form):
        mailing = form.save()
        return redirect('mailing_detail', pk=mailing.pk)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(mailing=self.object)
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing')
    extra_context = {
        'title': 'Удаление записи:'
    }

    def get_object(self, queryset=None):
        title = super().get_object(queryset)
        mailing = get_object_or_404(BlogPost, title=title)
        user_groups = [group.name for group in self.request.user.groups.all()]
        if mailing.owner != self.request.user and 'Managers' not in user_groups:
            raise Http404
        return mailing


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/create_message.html'

    def form_valid(self, form):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['mailing_pk'])
        message = form.save(commit=False)
        message.mailing = mailing
        message.save()
        return redirect('mailing_detail', pk=mailing.pk)


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['title'] = "Создание нового клиента."
        return data

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()

        return super().form_valid(form)


class DeliveryReportView(ListView):
    model = Log
    template_name = 'mailing/delivery_report.html'
    context_object_name = 'delivery_logs'

    def get_queryset(self):
        return Log.objects.filter(status='success')
