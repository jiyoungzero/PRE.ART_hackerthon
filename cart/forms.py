from email.policy import default
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    realname = forms.CharField(
        label = '작가 본명',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'작가 본명', 'style':'border: none;outline: none; -webkit-appearance: none;'}
        ),
        required=True,
    )
    artist_name = forms.CharField(
        label = '작가 활동명',
        widget = forms.TextInput(
            attrs = {'placeholder':'작가 활동명', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    team = forms.CharField(
        label = '작가 소속',
        widget = forms.TextInput(
            attrs = {'placeholder':'작가 소속', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    email = forms.EmailField(
        label = '작가 이메일',
        widget = forms.EmailInput(
            attrs = {'placeholder':'작가 이메일', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    artist_intro = forms.CharField(
        label = '작가 한줄 소개',
        widget = forms.TextInput(
            attrs = {'placeholder':'작가 한줄 소개', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    post_intro = forms.CharField(
        label = '전시 한줄 소개',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 한줄 소개', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )
    post_plan = forms.CharField(
        label = '전시 기획 의도',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 기획 의도', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )

    post_price = forms.DecimalField(
        label = '전시 목표 가격',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 목표 가격', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )

    post_place = forms.CharField(
        label = '전시 장소',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 장소', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )

    option = forms.ChoiceField(
        label = '승인상태(승인대기 선택)',
        choices=Post.option_choices,
    )

    class Meta:
        model = Post
        fields = [
            'realname', 'artist_name', 'team', 'email', 'artist_intro', 'post_intro', 'post_plan', 'option', 'post_price', 'post_place'
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
        post_price = cleaned_data.get('post_price', '')
        post_place = cleaned_data.get('post_place', '')
        option = cleaned_data.get('option', '')

        if option == '승인 완료':
            self.add_error('option', '승인 대기를 선택해주세요.')
        else:
            self.realname = realname
            self.artist_name = artist_name
            self.team = team
            self.email = email
            self.artist_intro = artist_intro
            self.post_intro = post_intro
            self.post_plan = post_plan
            self.post_price = post_price
            self.post_place = post_place
            self.option = option


class PosteidtForm(forms.ModelForm):
    realname = forms.CharField(
        label = '작가 본명',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'작가 본명', 'style':'border: none;outline: none; -webkit-appearance: none;'}
        ),
        required=True,
    )
    artist_name = forms.CharField(
        label = '작가 활동명',
        widget = forms.TextInput(
            attrs = {'placeholder':'작가 활동명', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    team = forms.CharField(
        label = '작가 소속',
        widget = forms.TextInput(
            attrs = {'placeholder':'작가 소속', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    email = forms.EmailField(
        label = '작가 이메일',
        widget = forms.EmailInput(
            attrs = {'placeholder':'작가 이메일', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    artist_intro = forms.CharField(
        label = '작가 한줄 소개',
        widget = forms.TextInput(
            attrs = {'placeholder':'작가 한줄 소개', 'style':'border: none;outline: none; -webkit-appearance: none;'}

        ),
        required=True,
    )
    post_intro = forms.CharField(
        label = '전시 한줄 소개',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 한줄 소개', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )
    post_plan = forms.CharField(
        label = '전시 기획 의도',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 기획 의도', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )

    post_price = forms.DecimalField(
        label = '전시 목표 가격',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 목표 가격', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )

    post_place = forms.CharField(
        label = '전시 장소',
        widget = forms.TextInput(
            attrs = {'placeholder':'전시 장소', 'style':'border: none;outline: none; -webkit-appearance: none;'}

                ),
        required=True,
    )

    option = forms.ChoiceField(
        label = '승인상태(관리자용)',
        choices=Post.option_choices,
    )

    class Meta:
        model = Post
        fields = [
            'realname', 'artist_name', 'team', 'email', 'artist_intro', 'post_intro', 'post_plan', 'option', 'post_price', 'post_place'
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
        post_price = cleaned_data.get('post_price', '')
        post_place = cleaned_data.get('post_place', '')
        option = cleaned_data.get('option', '')

        self.realname = realname
        self.artist_name = artist_name
        self.team = team
        self.email = email
        self.artist_intro = artist_intro
        self.post_intro = post_intro
        self.post_plan = post_plan
        self.post_price = post_price
        self.post_place = post_place
        self.option = option