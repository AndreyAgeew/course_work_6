from random import sample
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from blog.models import BlogPost
from .models import Mailing, Client, Message, Log
from .forms import MailingForm, MessageForm


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
        return context


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


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class DeliveryReportView(ListView):
    model = Log
    template_name = 'mailing/delivery_report.html'
    context_object_name = 'delivery_logs'

    def get_queryset(self):
        return Log.objects.filter(status='success')
