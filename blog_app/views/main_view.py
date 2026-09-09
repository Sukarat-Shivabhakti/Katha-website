from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from blog_app.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from blog_app.forms import ProfileUpdateForm


def index_method(request):
    # 1. Grab all posts by default
    posts = Post.objects.filter(status='published').order_by('-created_at')

    # 2. Check if the user is searching or clicking a category
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', 'All')

    # 3. Apply the Search Filter
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) | 
            Q(author__username__icontains=search_query)
        )

    # 4. Apply the Category Filter
    if category_filter and category_filter != 'All':
        posts = posts.filter(category__iexact=category_filter)

    # 5. Send the active filters back to the HTML so we can highlight them
    context = {
        'posts': posts,
        'search_query': search_query,
        'current_category': category_filter,
    }
    
    return render(request, 'main/index.html', context)


@login_required
def add_post_method(request):
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        content= request.POST.get("content")
        image = request.FILES.get("image")
        
        # 1. Grab the action from the button they clicked (publish or draft)
        action = request.POST.get("action")
        
        # 2. Determine the status based on the action
        post_status = 'published' if action == 'publish' else 'draft'

        # 3. Create the post and save the new status
        Post.objects.create(
            title=title,
            category=category,
            content=content,
            image=image,
            author=request.user,
            status=post_status 
        )

        # 4. Show the correct success message based on what they did
        if post_status == 'draft':
            messages.success(request, "Draft saved successfully! It is hidden from the main feed.")
            return redirect("index") # We can change this to redirect to a 'profile' page later!
        else:
            messages.success(request, "Story published successfully!")
            return redirect("index")

    return render(request, 'main/add_post.html')



def full_article_method(request, id):
    # Fetch the exact post using its ID
    post = get_object_or_404(Post, id=id)

    # Send that single post to the new HTML page
    return render(request, 'main/full_article.html', {'post': post})


def edit_post_method(request, id):
    # 1. Fetch the specific post
    post = get_object_or_404(Post, id=id)

    # 2. SECURITY: Kick out anyone who isn't the author
    if request.user != post.author:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('full_article', id=post.id)

    # 3. Handle the form submission
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.category = request.POST.get('category')
        post.content = request.POST.get('content')

        # 4. The Image Trick: Handle new uploads OR deletions
        new_image = request.FILES.get('image')
        remove_image = request.POST.get('remove_image') # Checks if the box was ticked

        if new_image:
            post.image = new_image
        elif remove_image == 'true':
            post.image = None # This deletes the image from the post!


            
        # 5. --- NEW DRAFT LOGIC ---
        action = request.POST.get('action')
        if action == 'publish':
            post.status = 'published'
            messages.success(request, "Story published to the Community Feed!")
            post.save()
            return redirect('full_article', id=post.id)
        elif action == 'draft':
            post.status = 'draft'
            messages.success(request, "Saved as Private Draft.")
            post.save()
            return redirect('profile', username=request.user.username)
        else:
            # Fallback just in case
            post.save()
            return redirect('profile', username=request.user.username)

    # 6. If it's a GET request, show the form
    return render(request, 'main/edit_post.html', {'post': post})


def delete_post_method(request, id):
    post = get_object_or_404(Post, id=id)

    # SECURITY: Only delete if the logged-in user wrote it
    if request.user == post.author:
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('index') # Sends them back to dashboard
    else:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('full_article', id=post.id)
    

def profile_method(request, username):
    # 1. Find the specific user by their username
    profile_user = get_object_or_404(User, username=username)
    
    # 2. Grab PUBLIC posts (Only 'published' status)
    user_posts = Post.objects.filter(author=profile_user, status='published').order_by('-created_at')
    post_count = user_posts.count()
    
    # 3. Grab DRAFTS (Security: ONLY if the logged-in user is looking at their OWN profile!)
    draft_posts = None
    if request.user == profile_user:
        draft_posts = Post.objects.filter(author=profile_user, status='draft').order_by('-created_at')
    
    # 4. Send both lists to the profile page
    context = {
        'profile_user': profile_user,
        'user_posts': user_posts,        # Public stories
        'draft_posts': draft_posts,      # Private drafts (will be None for strangers)
        'post_count': post_count
    }
    
    return render(request, 'main/profile.html', context)

#For about section
def about_method(request):
    return render(request, 'main/pages/about.html')

#For Privacy and Policies
def privacy_method(request):
    return render(request, 'main/pages/privacy.html')

#For terms of service 
def terms_method(request):
    return render(request, 'main/pages/terms.html')


@login_required
def edit_profile(request):
    # If the user hit the "Save" button
    if request.method == 'POST':
        # request.FILES is absolutely critical here for the image upload!
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            # Redirect back to their own profile page after saving
            return redirect('profile', username=request.user.username) 
    else:
        # If they just visited the page, show the form pre-filled with their current info
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'main/edit_profile.html', {'form': form})