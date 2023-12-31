from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Post
from .forms import CommentForm


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

class PostDetailView(View):
    def is_stored_post(self, post_request, post_id):
        stored_posts = post_request.session.get("stored_posts")
        if stored_posts is not None and post_id in stored_posts:
            is_saved_for_later = True
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            # commit=False instead of saveing the comment_form just creates a model instance
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": comment_form,
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # self.object points to the loaded post
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     # tags has a many2many relationship with Post and its an object containing all the tags
#     # by using all() then we recieve a list which is iterable
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
