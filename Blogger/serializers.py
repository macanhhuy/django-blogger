from rest_framework import serializers
from .models import Post, Author


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes the Post model"""
    author = serializers.HyperlinkedRelatedField(source='author', view_name=
                                                 'author-detail')
    tags = serializers.ManyRelatedField(source='tags')

    class Meta:
        model = Post
        fields = ('url', 'author', 'title', 'body',
                  'created_at', 'published', 'tags',
                  'slug')

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.author = attrs['author']
            instance.title = attrs['title']
            instance.body = attrs['body']
            instance.published = attrs['published']
            # TODO: this is doable. probably need to
            # split on , and do .set for each
            #instance.tags = attrs['tags'] 
            # TODO: 'slugify' with django
            instance.slug = attrs['slug']
            return instance
        return Post(**attrs)


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes the Author model"""

    class Meta:
        model = Author
        fields = ('url', 'username','first_name', 'last_name', )
