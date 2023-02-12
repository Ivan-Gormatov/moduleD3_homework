from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    
    def update_rating(self):

        postRat=Post.objects.filter(author=self).aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        
        commentRat=Comment.objects.filter(commentUser=self.authorUser).aggregate(commentRating=Sum('rating')) 
        cRat=0
        cRat += commentRat.get('commentRating')
        
        commPostRat=Comment.objects.filter(commentPost__author=self).aggregate(commPostRating=Sum('rating'))
        cPRat=0
        cPRat += commPostRat.get('commPostRating')
        
        self.ratingAuthor = pRat*3 + cRat + cPRat
        self.save()
        

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статаья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreat = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return f'{self.author.authorUser}:  {self.title.title()}- {self.categoryType}'
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()
        
    def preview(self):
        return self.text[0:124] + '...'
    

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreat = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return self.commentUser.username
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()