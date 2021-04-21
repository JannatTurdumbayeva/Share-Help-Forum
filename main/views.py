from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from account import serializers, models
from .models import Problem, Reply, Comment, Favorite, Rating, History, Like
from .parsing import pars

from .serializers import ProblemSerializer, ReplySerializer, CommentSerializer, LikeSerializer, \
    FavoriteSerializer, RatingSerializer, HistorySerializer, ParsSerializer
from .permission import IsAuthorPermission



class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated,]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProblemViewSet(PermissionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @action(methods = ['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        serializer = self.get_serializer(queryset,
                                         many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods = ['GET'], detail=False)
    def sort(self, request):
        filter = request.query_params.get('filter')
        if filter == 'A-Z':
            queryset = self.get_queryset().order_by('title')
        elif filter == 'Z-A':
            queryset = self.get_queryset().order_by('-title')
        elif filter == 'replies':
            maximum = 0
            for problem in self.get_queryset():

                if maximum < problem.replies.count():
                    maximum = problem.replies.count()
                    queryset = self.get_queryset().filter(id=problem.id)
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class FavoriteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class RatingViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}



class ViewHistory(APIView):
    def get(self, request):
        user = request.user
        history = History.objects.filter(user=user).order_by('-created')
        serializer = HistorySerializer(instance=history, many=True)
        return Response(serializer.data)



class ParsOcView(APIView):
    def get(self, request):
        dict_ = pars()
        serializer = ParsSerializer(instance=dict_, many=True)
        return Response(serializer.data)