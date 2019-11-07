"""View module for handling requests about articles"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import Article, Coder


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for articles

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Article
        url = serializers.HyperlinkedIdentityField(
            view_name='article',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'synopsis', 'link', 'reference', 'coder_id')

        depth = 1

class Articles(ViewSet):
    """Articles for codeArchive"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Article instance
        """
        new_article = Article()
        new_article.title = request.data["title"]
        new_article.synopsis = request.data["synopsis"]
        new_article.link = request.data["link"]
        new_article.reference = request.data["reference"]
        new_article.coder = Coder.objects.get(user=request.auth.user)

        new_article.save()

        serializer = ArticleSerializer(new_article, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single article

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            article = Article.objects.get(pk=pk)
            article.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Article.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for an article

        Returns:
            Response -- Empty body with 204 status code
        """
        article = Article.objects.get(pk=pk)
        article.title = request.data["title"]
        article.synopsis = request.data["synopsis"]
        article.link = request.data["link"]
        article.reference = request.data["reference"]

        article.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single article

        Returns:
            Response -- JSON serialized article instance
        """
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to articles resource

        Returns:
            Response -- JSON serialized list of articles
        """
        articles = Article.objects.all()
        coder = Coder.objects.get(user=request.auth.user)
        articles = Article.objects.filter(coder=coder)

        serializer = ArticleSerializer(
            articles,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)