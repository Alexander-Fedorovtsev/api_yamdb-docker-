import datetime as dt

from django.db.models import Avg

from rest_framework import serializers, validators

from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment, Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 <= value <= year):
            raise serializers.ValidationError(
                'Год не может быть больше текущего!'
            )
        return value


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=None)
    score = serializers.IntegerField(max_value=10, min_value=1, default=0)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date", "title")

    validators = [
        validators.UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['author', 'title'],
            message='Вы уже оставляли отзыв к этому произведению.'
        )
    ]

    def validate(self, params):
        review = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id'))
        if review.exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя добавить второй отзыв на то же самое произведени')
        return params


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
