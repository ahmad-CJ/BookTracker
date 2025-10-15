from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book, Review
from .forms import BookForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404


# class to prevent access to other books
class UserAccessMixin(UserPassesTestMixin):
    def test_func(self):
        book = self.get_object()
        return book.user == self.request.user
    
    def handle_no_permission(self):
        raise Http404("Book not found")
# signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to BookTracker! 🎉')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})
# logout
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully! 👋')
    return redirect('home')



def about(request):
  return render(request, 'about.html')


class BookList(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    
    # Returns all books from the database (Book.objects.all()) and sorts them by creation date (created_at) in descending order
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user).order_by('-created_at')
                             
class BookDetail(UserAccessMixin, LoginRequiredMixin, DetailView):  # most be sorted like this
    model = Book
    template_name = 'books/book_detail.html'

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list') #to return me to all books (book_list)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Book added successfully! 📚')
        return super().form_valid(form)

                       #+
class BookUpdate(UserAccessMixin, LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')
  
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully! ✏️')
        return super().form_valid(form)     # Save data in database

class BookDelete(UserAccessMixin, LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book deleted successfully! 🗑️') # Succecfully delete messege for user

        # Delete the book from the database
        return super().delete(request, *args, **kwargs)

# Rating and Review part
# To get the book to which the review will be added based on the book_id passed through the URL
# If the book is not found in the database, Django will display a 404 page
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)

    if request.method == 'POST':
       # Data entered by the user is fetched via the form
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

       # It checks whether the required fields have been filled in. If all fields are complete, a new review is created
        if rating and comment:
            Review.objects.create(
                book=book,
                rating=int(rating), # Convert the rating to an integer
                comment=comment
            )
            messages.success(request, 'Review added successfully! ⭐')
        else:
            messages.error(request, 'Please fill all fields')
    
    return redirect('book_detail', pk=book_id)

 # Reading status
def toggle_read_status(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    book.is_read = not book.is_read
    book.save()
    status = "Read" if book.is_read else "Unread"
    messages.success(request, f'Book status changed to: {status} 📖')
    return redirect('book_list')

# Home Page with statistics
def home(request):
    if request.user.is_authenticated:
        total_books = Book.objects.filter(user=request.user).count()
        read_books = Book.objects.filter(user=request.user, is_read=True).count()
        unread_books = Book.objects.filter(user=request.user, is_read=False).count()
    else:
        total_books = 0
        read_books = 0
        unread_books = 0
     
    stats = {
        'total_books': total_books,
        'read_books': read_books,
        'unread_books': unread_books,
    }
    
    return render(request, 'home.html', {'stats': stats})