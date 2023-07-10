
from django.db import models
from django.contrib import auth
from PIL import Image

# Create your models here.    
class Publisher(models.Model):
    
    """A company that publishes books."""
    name =models.CharField(max_length=50,help_text="The name of the Publisher.")
    website=models.URLField(help_text="The Publisher's website.")
    email=models.EmailField(help_text="The Publisher's email address.")
    def __str__(self):
        return self.name
    
class Book(models.Model):
    
    """A published book."""
    title=models.CharField(max_length=70,help_text="The title of the book.")
    publication_date=models.DateTimeField(verbose_name="Date the book was published.")
    isbn=models.CharField(max_length=20,verbose_name="ISBN number of the book.")
    # Many to one relationship
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE)
    # Many to many relationship
    contributor=models.ManyToManyField('Contributor',through='BookContributor')
    sample=models.FileField( upload_to='book_samples/%Y/%m/%d/', max_length=100, null=True , blank=True)
    cover=models.ImageField( upload_to="book_cover/%Y/%m/%d/", null=True , blank=True )
    
    # takes a method (or a non-field attribute) of the model class, 
    # such as __str__, as long as it accepts the model object as an argume
    def isbn13(self):
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(self.isbn[0:3], self.isbn[3:4],
                                       self.isbn[4:6], self.isbn[6:12],self.isbn[12:13])
    # Override save method on model to resize image instead of views
    # def save(self, *args, **kwargs):
    #     # Read image
    #     img=Image.open(self.cover.path)
    #     # Resize Image
    #     img.thumbnail((300,300))
    #     # Save image
    #     img.save(self.cover.path)
        
    #     super().save(*args, **kwargs)
       
    def __str__(self):
        return self.title
        #return "{} ({})".format(self.title, self.isbn13())
    
class Contributor(models.Model):
    
    """A contributor to a Book, e.g. author, editor, co-author."""
    first_names=models.CharField(max_length=50,help_text="The contributor's first name or names.")
    last_names=models.CharField(max_length=50,help_text="The contributor's last name or names.")
    email=models.EmailField(help_text="The contact email for the contributor.")
    
    def initialled_name(self):
        sec_part=''.join([name[0] for name in self.first_names.split(" ")])
        return f'{self.last_names}, {sec_part}'
    
    def __str__(self):
        return self.initialled_name()
    def number_of_contributions(self):
        books=self.book_set.count()
        return books

class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHER='AUTHOR' , 'Author'
        CO_AUTHOR='CO_AUTHOR' , 'Co-Author'
        EDITOR='EDITOR' , 'Editor'
    
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    contributor=models.ForeignKey(Contributor,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,verbose_name='The role this contributor had in the book.',
                          choices=ContributionRole.choices)

class Review(models.Model):
    content=models.TextField(help_text="The Review text.")
    rating=models.IntegerField(help_text="The rating the reviewer has given.")
    date_created=models.DateTimeField(auto_now_add=True,help_text="The date and time the review was created.")
    date_edited=models.DateTimeField(null=True,help_text="The date and time the review was last edited.")
    # One to one relationship
    creator=models.ForeignKey(auth.get_user_model(),on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,help_text="The Book that this review is for.")
    def __str__(self):
        return self.content