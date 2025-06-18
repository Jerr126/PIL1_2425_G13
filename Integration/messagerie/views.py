from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message
from django.contrib.auth.models import User

@login_required
def index(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messagerie/index.html', {'conversations': conversations})

@login_required
def conversation(request, conversation_id):
    conv = Conversation.objects.get(id=conversation_id)
    if request.user not in conv.participants.all():
        return redirect('index')
    
    messages = Message.objects.filter(conversation=conv).order_by('timestamp')
    return render(request, 'messagerie/conversation.html', {
        'conversation': conv,
        'messages': messages,
    })

@login_required
def start_conversation(request, user_id):
    recipient = User.objects.get(id=user_id)
    # Vérifier si une conversation existe déjà
    conv = Conversation.objects.filter(participants=request.user).filter(participants=recipient).first()
    
    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(request.user, recipient)
    
    return redirect('conversation', conversation_id=conv.id)

@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        conv = Conversation.objects.get(id=conversation_id)
        if request.user not in conv.participants.all():
            return JsonResponse({'status': 'error', 'message': 'Not authorized'})
        
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                conversation=conv,
                sender=request.user,
                content=content
            )
            return JsonResponse({
                'status': 'success',
                'message': {
                    'content': message.content,
                    'sender': message.sender.username,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M'),
                }
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


