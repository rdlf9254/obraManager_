# Django imports
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt

# REST framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

# JWT Token imports
from rest_framework_simplejwt.tokens import RefreshToken

# Local models imports
from .models import usuario, visualizarProjeto, projeto, fotoProjeto, dataGrafico

# Other imports
import json


from .models import usuario

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        # Coletar informações de login do corpo da solicitação
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email is None or password is None:
            return Response({'error': 'Por favor, forneça tanto o email quanto a senha'},
                            status=status.HTTP_400_BAD_REQUEST)

        
        # Autenticar o usuário
        user = authenticate(username=email, password=password)  # Correção aqui

        # Verificar se o usuário existe e as credenciais estão corretas
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'success': True,
                'message': 'Login bem-sucedido',
                'access_token': access_token,
                'id': getattr(user, 'id', None),
                'username': getattr(user, 'username', None),
                'first_name': getattr(user, 'first_name', None),
                'last_name': getattr(user, 'last_name', None),
                'date_joined': getattr(user, 'date_joined', None),
                'email': getattr(user, 'email', None),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    @api_view(['GET'])
    def get_user_details(request, user_id):

        try:
            user = usuario.objects.get(id=user_id)
            return JsonResponse(model_to_dict(user))
        except usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)


class Usuarios(APIView):
    @csrf_exempt
    def create_user(request):
        if request.method == "POST":
            data = json.loads(request.body)

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )

            user_type = data['type']['id']

            user_extended = usuario.objects.create(
                user=user,
                useType=user_type,
                usePhoto=data.get('photo', ''),
            )

        for project_id in data['projects']:
            proj = get_object_or_404(projeto, id=project_id)
            
            visualizarProjeto.objects.create(
                visUserId=user_extended,
                visProjId=proj
            )

            return JsonResponse({"message": "Usuário criado com sucesso!"}, status=201)

        return JsonResponse({"error": "Método não permitido"}, status=405)
    
    @csrf_exempt
    def get_name(request, **kwargs):

        try:
            u_id = kwargs.get('user_id', None)
            user = get_object_or_404(User, id=u_id)
            
            return JsonResponse({"success": True, 'first_name': user.first_name, 'last_name': user.last_name }, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro desconhecido: {str(e)}"}, status=500)

    @csrf_exempt
    def update_user(request):
        if request.method == "PUT":
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('id')

            user_obj = get_object_or_404(User, id=user_id)
            
            user_obj.first_name = data['first_name']
            user_obj.last_name = data['last_name']
            user_obj.username = data['username']
            user_obj.email = data['email']
            if data.get('password'):
                user_obj.set_password(data['password'])
            user_obj.save()

            user_extended = user_obj.usuario
            user_extended.useType = data['type']['id']
            user_extended.usePhoto = data.get('photo', '')
            user_extended.save()

            if data.get('projects'):
                for project_id in data['projects']:
                    proj = get_object_or_404(projeto, id=project_id)
                    
                    visualizarProjeto.objects.create(
                        visUserId=user_extended,
                        visProjId=proj
                    )

            return JsonResponse({"message": "Usuário atualizado com sucesso!"})

        return JsonResponse({"error": "Método não permitido"}, status=405)

    def get_users(request):
        if request.method == "GET":
            users = User.objects.select_related('usuario').all()

            user_list = []

            for user in users:
                user_dict = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'date_joined': user.date_joined,
                }

                # Verifique se o objeto User tem um objeto usuario relacionado
                if hasattr(user, 'usuario'):
                    user_dict['useType'] = user.usuario.useType
                    user_dict['usePhoto'] = user.usuario.usePhoto

                user_list.append(user_dict)

            return JsonResponse({'users': user_list})
    @csrf_exempt
    def delete_user(request):

        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('id')

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"success": True, "message": "Usuário deletado com sucesso"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "Usuário não encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro desconhecido: {str(e)}"}, status=500)


class Projects (APIView):
    def all_projects(request):
        if request.method == "GET":
            projects = projeto.objects.all()
            data = [{
                'id': proj.proId,
                'name': proj.proName,
                'address': proj.proAddress,
                'status': proj.proStatus,
                'createdAt': proj.proCreatedAt.strftime('%Y-%m-%d %H:%M:%S.%f'), 
                'lastUpdate': proj.proLastUpdate.strftime('%Y-%m-%d %H:%M:%S.%f'),
                'stage': proj.proStage,
                'generalProgress': proj.proGeneralProgress,
                'stageProgress': proj.proStageProgress,
                'nextStageProgress': proj.proNextStageProgress,
                'totalTasks': proj.proTotalTasks,
                'doneTasks': proj.proDoneTasks,
                'doingTasks': proj.proDoingTasks,
                'responsibleId': proj.proResponsible_id,
                'creatorId': proj.proUseCreator_id
            } for proj in projects]

            return JsonResponse(data, safe=False, status=200)

        return JsonResponse({"error": "Método não permitido"}, status=405)
    
    def all_projects_names(request):
        if request.method == "GET":
            projects = projeto.objects.all()
            data = [{
                'id': proj.proId,
                'label': proj.proName,
            } for proj in projects]

            return JsonResponse(data, safe=False, status=200)

        return JsonResponse({"error": "Método não permitido"}, status=405)


    def my_projects(request, id):
        if request.method == "GET":
            viewed_projects_ids = visualizarProjeto.objects.filter(visUserId_id=id).values_list('visProjId_id', flat=True)
            projects = projeto.objects.filter(proId__in=viewed_projects_ids)
            data = [{
                'id': proj.proId,
                'name': proj.proName,
                'address': proj.proAddress,
                'status': proj.proStatus,
                'createdAt': proj.proCreatedAt.strftime('%Y-%m-%d %H:%M:%S.%f'), 
                'lastUpdate': proj.proLastUpdate.strftime('%Y-%m-%d %H:%M:%S.%f'), 
                'stage': proj.proStage,
                'generalProgress': proj.proGeneralProgress,
                'stageProgress': proj.proStageProgress,
                'nextStageProgress': proj.proNextStageProgress,
                'totalTasks': proj.proTotalTasks,
                'doneTasks': proj.proDoneTasks,
                'doingTasks': proj.proDoingTasks,
                'responsibleId': proj.proResponsible_id,
                'creatorId': proj.proUseCreator_id
            } for proj in projects]

            return JsonResponse(data, safe=False, status=200)

        return JsonResponse({"error": "Método não permitido"}, status=405)
    
    def get_project_by_id(request, project_id):
        try:
            proj = get_object_or_404(projeto, proId=project_id)
            photos = fotoProjeto.objects.filter(phoProjId=proj)
            graph_data = dataGrafico.objects.filter(graProjId=proj)
            
            proj_serialized = json.loads(serialize('json', [proj]))[0]['fields']
            photos_serialized = json.loads(serialize('json', photos))
            graph_data_serialized = json.loads(serialize('json', graph_data))
            
            proj_serialized['photos'] = [photo['fields'] for photo in photos_serialized]
            proj_serialized['graph_data'] = [data['fields'] for data in graph_data_serialized]
            
            return JsonResponse({"success": True, "data": proj_serialized}, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro desconhecido: {str(e)}"}, status=500)

class UploadFotoProjetoView(APIView):
    @csrf_exempt
    def upload_photo(request):
        if request.method == "POST":
            try:
                phoBase = request.data.get("phoBase")
                phoProjId = request.data.get("phoProjId")
                if phoBase and phoProjId:
                    foto = fotoProjeto(
                        phoBase=phoBase,
                        phoProjId_id=phoProjId
                    )
                    foto.save()
                    return JsonResponse({"message": "Foto adicionada com sucesso!", "status": "success"})
                else:
                    return JsonResponse({"message": "Parâmetros inválidos", "status": "error"}, status=400)
                    
            except Exception as e:
                return JsonResponse({"message": str(e), "status": "error"}, status=500)
