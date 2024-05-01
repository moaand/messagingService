from datetime import datetime
from .models import Message, User
from .serializers import MessageSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def get_messages(receiver, startdate, enddate):

    receiverSerializer = UserSerializer(receiver)
    receiverId = receiverSerializer.data['id']
    dateAccessed = receiverSerializer.data['date_accessed']

    messages = Message.objects.filter(receiver=receiverId)

    if startdate or enddate:
        if startdate:
            messages = messages.filter(created_at__gte=startdate)
        if enddate:
            messages = messages.filter(created_at__lte=enddate)
    elif not dateAccessed == None:
        messages = messages.filter(created_at__range=[dateAccessed, datetime.now()])

    serializer = MessageSerializer(messages, many=True)

    receiverSerializer = UserSerializer(receiver, data={'date_accessed': datetime.now()}, partial=True)
    if receiverSerializer.is_valid():
        receiverSerializer.save()
    
    return Response(serializer.data)

def send_message(receiver, data):
    
    if not User.objects.filter(name=data['sender']).exists() or data['content'] == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    sender = User.objects.get(name=data['sender'])
    content = data['content']

    receiverId = UserSerializer(receiver).data['id']
    senderId = UserSerializer(sender).data['id']

    serializer = MessageSerializer(data={'content':content, 'sender':senderId, 'receiver': receiverId})

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def delete_messages(receiver):

    receiverId = UserSerializer(receiver).data['id']

    messages = Message.objects.filter(receiver=receiverId)

    messages.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def messages(request, name):

    if not User.objects.filter(name=name).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    receiver = User.objects.get(name=name)
    
    if request.method == 'GET':
        return get_messages(receiver=receiver, startdate=request.GET.get("startdate"), enddate=request.GET.get("enddate"))
         
    elif request.method == 'POST':
        return send_message(receiver=receiver, data=request.data)

    elif request.method == 'DELETE':
        return delete_messages(receiver=receiver)

@api_view(['DELETE'])
def delete_message(_, id):
    message = Message.objects.get(id=id)
    message.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def users(request):

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        if User.objects.filter(name=request.data['name']).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(data=request.data)
        
        if request.data['name'] == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)