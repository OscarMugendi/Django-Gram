from django.test import TestCase
from . models import Image, Profile, Comment, Like

# Create your tests here.

class ProfileTestClass(TestCase):
    
    def setUp(self):
        self.profile = Profile(profile_photo ='test_profile_pic', bio = 'test_bio')

    def test_save_profile(self):
        self.profile.save_profile()
        all_profiles = Profile.objects.all()
        self.assertTrue(len(all_profiles)>0)

        
    def test_delete_profile(self):
        self.profile.save_profile()
        profile2 = Profile(profile_photo ='test_profile_pic2',bio = 'test_bio2')
        profile2.save_profile()

        self.profile.delete_profile()
        all_profiles = Profile.objects.all()
        self.assertTrue(len(all_profiles)==1)


class ImageTestClass(TestCase):

    def setUp(self):
        self.image = Image(image = 'test_url',image_name ='test_image' , caption='test_caption',)

    def test_instance(self):
        self.assertTrue(isinstance(self.image,Image)) 

    def test_save_image(self):
        self.image.save_image()
        all_images= Image.objects.all()
        self.assertTrue(len(all_images)>0)

    def test_delete_images(self):
        self.image.save_image()
        new_image = Image(image = 'test_url2',image_name ='test_image2' , caption='test_caption2',)
        new_image.save_image()

        self.image.delete_image()
        all_images = Image.objects.all()
        self.assertTrue(len(all_images)==1)

    def test_update_caption(self):
        self.image.save_image()
        image = Image.objects.get(image ='test_url')
        image.update_caption('new caption')
        image = Image.objects.get(image ='test_url')

        self.assertTrue(image.caption=='new caption')


class CommentTestClass(TestCase):

    def setUp(self):
        self.new_comment = Comment(comment= "Test comment")
        self.new_comment.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))

    def test_save_comment(self):
        self.new_comment.save_comment()
        all_comments = Comment.objects.all()
        self.assertTrue(len(all_comments)>0)

        
    def test_delete_comment(self):
        self.new_comment.save_comment()
        comment2 = Comment(comment='Second test comment')
        comment2.save_comment()

        self.new_comment.delete_comment()
        all_comments = Comment.objects.all()
        self.assertTrue(len(all_comments)==1)