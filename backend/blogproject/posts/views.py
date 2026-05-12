from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_post(request, pk):
    try:
        post = Post.objects.get( id = pk)
    except Post.DoesNotExist:
        return Response(
            {"error":"Post not found."},
            status= status.HTTP_404_NOT_FOUND
        )
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_posts(request):
    serializer = PostSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(author = request.user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_post(request, pk):
    try:
        post = Post.objects.get(id = pk)
    except Post.DoesNotExist:
        return Response(
        {"error": "Post not found"},
        status = status.HTTP_404_NOT_FOUND )
    
    serializer = PostSerializer(
        post,
        data = request.data,
        partial= True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status= status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
def delete_post(request, pk):
    try:
        post = Post.objects.get(id = pk)
    except Post.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status= status.HTTP_404_NOT_FOUND
        )
    
    post.delete()

    return Response(status= status.HTTP_204_NO_CONTENT)

