from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    realname = forms.CharField(
        label = '작가 본명',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'작가 본명'}
        ),
        required=True,
    )
    artist_name = forms.CharField(
        label = '작가 활동명',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'작가 활동명'}
        ),
        required=True,
    )
    team = forms.CharField(
        label = '작가 소속',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'작가 소속'}
        ),
        required=True,
    )
    email = forms.EmailField(
        label = '작가 이메일',
        widget = forms.EmailInput(
            attrs = {
                'placeholder':'작가 이메일'}
        ),
        required=True,
    )
    artist_intro = forms.CharField(
        label = '작가 한줄 소개',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'작가 한줄 소개'}
        ),
        required=True,
    )
    post_intro = forms.CharField(
        label = '전시 한줄 소개',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'전시 한줄 소개'}
                ),
        required=True,
    )
    post_plan = forms.CharField(
        label = '전시 기획 의도',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'전시 기획 의도'}
                ),
        required=True,
    )

    class Meta:
        model = Post
        fields = [
            'realname', 'artist_name', 'team', 'email', 'artist_intro', 'post_intro', 'post_plan'
        ]

    def clean(self):
        cleaned_data = super().clean()

        realname = cleaned_data.get('realname', '')
        artist_name = cleaned_data.get('artist_name', '')
        team = cleaned_data.get('team', '')
        email = cleaned_data.get('email', '')
        artist_intro = cleaned_data.get('artist_intro', '')
        post_intro = cleaned_data.get('post_intro', '')
        post_plan = cleaned_data.get('post_plan', '')

        self.realname = realname
        self.artist_name = artist_name
        self.team = team
        self.email = email
        self.artist_intro = artist_intro
        self.post_intro = post_intro
        self.post_plan = post_plan