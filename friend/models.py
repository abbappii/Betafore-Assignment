from django.db import models
from feed.initials import Initials

class FriendList(models.Model):
    user = models.OneToOneField('account.User',on_delete=models.CASCADE, related_name='friend_list_user')
    friends = models.ManyToManyField('account.User',blank = True, related_name='friends')

    def __str__(self):
        return self.user.username
    
    def add_friend(self,account):
        "add friend"
    
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self,removee):
        remover_friends_list = self
        remover_friends_list.remove(removee)

        # remove friend from removee friend list 
        friend_list = FriendList.objects.get(user=removee)
        friend_list.remove_friend(self.user)

    def is_mutual_friend(self,friend):
        # is this a friend 
        if friend in self.friends.all():
            return True
        return False

class FriendRequests(Initials):
    # person who receive request 
    # and who send request

    sender = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='receiver')

    def __str__(self):
        return self.sender.username

    def accept(self):
        print('self in model accept:',self)
        
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)

            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active  = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()





