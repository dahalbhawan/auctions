from .models import Listing, Bid, Comment
from django.forms import ModelForm, Textarea, FloatField, NumberInput

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','category','list_price','image_url']
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BidForm(ModelForm):
    bid_price = FloatField(widget=NumberInput(attrs={'placeholder': 'Bid Price'}))
    class Meta:
        model = Bid
        fields = ['bid_price']
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'