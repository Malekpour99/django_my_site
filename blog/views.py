from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    # instead of using 'model', 'ordering' and 'get_queryset' you can use 'queryset'
    # queryset = Post.objects.all().order_by("-date")[:3]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })


class PostsView(ListView):
    template_name = "blog/all-posts.html"
    queryset = Post.objects.all().order_by("-date")
    context_object_name = "all_posts"


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#         "all_posts": all_posts
#     })

class PostDetailView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object points to the loaded post
        context["post_tags"] = self.object.tags.all()
        return context


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     # tags has a many2many relationship with Post and its an object containing all the tags
#     # by using all() then we recieve a list which is iterable
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })
