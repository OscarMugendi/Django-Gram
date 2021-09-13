from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.

class Profile(models.Model):
    '''
    A class that defines the structure of each profile.
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=30,default='User')
    profile_photo = models.ImageField(blank=True,upload_to = 'images/', null=True)
    bio = models.TextField(max_length = 255,blank=True)

    def __str__(self):
        return f'{self.user.username}'

    def save_profile(self):
            self.save()

    def delete_profile(self):
        self.delete()


    @classmethod
    def find_profile(cls,name):
        profiles_found = cls.objects.filter(username__icontains = name).all()
        return profiles_found



class Image(models.Model):
    '''
    A class that defines the structure of each image.
    '''

    image = models.ImageField(upload_to="images/",null = True )
    image_name = models.CharField(max_length =30,null = True ) 
    caption = models.TextField(null = True )
    pub_date = models.DateTimeField(auto_now_add=True, null= True)
    profile_key = models.ForeignKey(Profile,on_delete=models.CASCADE, null = True)
    user_key = models.ForeignKey(User,on_delete= models.CASCADE , null = True)
    likes = models.PositiveIntegerField(default=0)
    comments_number = models.PositiveIntegerField(default=0)
        
    def __str__(self):
        return self.image_name 

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete() 

    def update_caption(self,new_caption):
        self.caption = new_caption
        self.save()

    @classmethod
    def get_image_by_id(cls,id):
        image_by_id = Image.objects.get(id = id)
        return image_by_id

    @classmethod
    def get_images_by_user(cls,id):
        user_images = Image.objects.filter(user_id=id)
        return user_images

    class Meta:
        ordering = ['-pub_date']

    @classmethod
    def get_all_images(cls):
        all_posted_images = cls.objects.all()
        return all_posted_images 

    @classmethod
    def get_timeline_posts(cls):
        '''
        A function that gets all images posted by those being followed the user.
        '''
        timeline_posts = Image.objects.filter()



class Comment(models.Model):
    '''
    A class that defines the structure of a comment.
    '''

    user_id = models.ForeignKey(User,on_delete=models.CASCADE, null= True)
    image_id = models.ForeignKey(Image,on_delete=models.CASCADE, null= True)
    comment= models.TextField(blank=True)

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()


class Like(models.Model):
    '''
    A class that defines the structure of a like.
    '''

    user = models.ForeignKey(User,on_delete=models.CASCADE, null= True)
    image = models.ForeignKey(Image,on_delete=models.CASCADE, null = True)

    def __int__(self):
        return self.user.username

    def save_like(self):
        self.save() 

    def delete_like(self):
        self.delete()

    def like(self):
        self.likes_number = 2
        self.save()

    @classmethod
    def get_likes(cls,image_id):
        likes = cls.objects.filter(image = image_id)
        return likes 



class Follow(models.Model):
    
    follower = models.ForeignKey(User,on_delete=models.CASCADE, null= True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, null= True)
    
    def __int__(self):
        return self.follower.username 
    
    def save_follower(self):
        self.save()

    @classmethod
    def get_followers(cls,profile_id):
        profile = Profile.objects.filter(id = profile_id)
        followers = cls.objects.filter(user= profile.user.id)
        return len(followers)