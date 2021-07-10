from django.views import generic
from .models import Post
from .filters import BlogFilter


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BlogFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'