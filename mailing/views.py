from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from .models import Mailing, Client, Message
from .forms import MailingForm, MessageForm


class MainView(TemplateView):
    template_name = 'mailing_service/main.html'
    extra_context = {
        'title': 'Главная страница',
        'object_list': Mailing.objects.all()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_posts = list(BlogEntry.objects.all())
        context['random_blog_posts'] = sample(all_posts, min(3, len(all_posts)))
        return context


class MailingCreateView(View):
    template_name = 'mailing/create_mailing.html'
    form_class = MailingForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            mailing = form.save()
            return redirect('mailing_detail', pk=mailing.pk)
        return render(request, self.template_name, {'form': form})


class MailingDetailView(View):
    template_name = 'mailing/mailing_detail.html'

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        messages = Message.objects.filter(mailing=mailing)
        return render(request, self.template_name, {'mailing': mailing, 'messages': messages})


class MessageCreateView(View):
    template_name = 'mailing/create_message.html'
    form_class = MessageForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, mailing_pk):
        mailing = get_object_or_404(Mailing, pk=mailing_pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.mailing = mailing
            message.save()
            return redirect('mailing_detail', pk=mailing.pk)
        return render(request, self.template_name, {'form': form})


class ClientListView(View):
    template_name = 'mailing/client_list.html'

    def get(self, request):
        clients = Client.objects.all()
        return render(request, self.template_name, {'clients': clients})


class MailingListView(View):
    template_name = 'mailing/home.html'

    def get(self, request):
        mailings = Mailing.objects.all()
        return render(request, self.template_name, {'mailings': mailings})
