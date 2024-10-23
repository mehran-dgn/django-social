from django.shortcuts import render , redirect 
from django.views import View 
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
# Create your views here.

class HomeView(View):
    def get(self , request):
        posts = Post.objects.all()
        return render(request,"home/index.html",{'posts':posts})
    
    def post(self,request):
        pass 

class PostDetailView(View):
    def get(self,request,post_id,post_slug):
        post = Post.objects.get(pk=post_id , slug=post_slug)
        return render(request, 'home/detail.html',{'post':post})
    
class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request , "Post deleted successfully" , 'success')
        else:
            messages.success(request,"You can't delete this post" , 'danger')

        return redirect("home:home")

class PostUpdateView(LoginRequiredMixin , View):
    form_class = PostUpdateForm

    def dispatch(self,request,*args,**kwargs):
        post = Post.objects.get(pk=kwargs['post_id'])
        if not post.user.id == request.user.id :
            messages.error(request,"You can't update this post" ,'danger')
            return redirect("home:home")

    def get(self,request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(instance = post)
        return render(request,"home/update.html" , {'form':form})

    def post(self,request , post_id ):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(request.POST , instance=post)
        if form.is_valid():
            form.save()
            messages.succes(request, 'You Updated this post' , 'success')
            return redirect("home:post_detail",post.id , post.slug)
