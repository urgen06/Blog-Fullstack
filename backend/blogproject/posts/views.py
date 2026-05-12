from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from .models import Post
from .serializers import PostSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print(request.data)       
    print(request.content_type)
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Username and Password required."},
            status= status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username = username).exists():
        return Response(
            {"error":"username already taken"},
            status= status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username= username, password= password)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "message" : "user created successfully",
            "access" : str(refresh.access_token),
            "refresh" : str(refresh)
        },
        status= status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    from django.contrib.auth import authenticate    
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username = username, password = password)
    if user is None:
        return Response(
            {'error':'Invalid Credentials'},
            status= status.HTTP_401_UNAUTHORIZED
        )
    
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
        }
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

