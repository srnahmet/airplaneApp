from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from uav_manufacturing_application.models import Employee, Team, PartType, UAVType

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # UAV Type'ları oluştur
        uav_types = [
            {'name': 'TB2'},
            {'name': 'TB3'},
            {'name': 'AKINCI'},
            {'name': 'KIZILELMA'}
        ]
        for uav_type in uav_types:
            UAVType.objects.create(**uav_type)

        # Part Type'ları oluştur
        part_types = [
            {'name': 'Kanat'},
            {'name': 'Gövde'},
            {'name': 'Kuyruk'},
            {'name': 'Aviyonik'}
        ]
        for part_type in part_types:
            PartType.objects.create(**part_type)

        # Takımların oluşturulması
        teams = [
            {'name': 'Kanat Takımı', 'part_type_id': 1},
            {'name': 'Gövde Takımı', 'part_type_id': 2},
            {'name': 'Kuyruk Takımı', 'part_type_id': 3},
            {'name': 'Aviyonik Takımı', 'part_type_id': 4},
            {'name': 'Montaj Takımı', 'is_montage_team': True}  # Montaj takımı
        ]
        for team in teams:
            part_type_id = team.get('part_type_id')
            part_type = None
            if part_type_id:
                part_type = PartType.objects.get(id=part_type_id)
            Team.objects.create(name=team['name'], part_type=part_type, is_montage_team=team.get('is_montage_team', False))

        # Süper kullanıcıyı oluştur
        superuser = User.objects.create_superuser(
            username='asirin',
            password='asirin',
            email='srnahmet98@gmail.com'
        )
        Employee.objects.create(user=superuser, name='Admin')

        # Kullanıcı bilgileri
        users_info = [
            {'username': 'asirin_kanat', 'name': 'Kanat Personeli', 'team_id': 1},
            {'username': 'asirin_govde', 'name': 'Gövde Personeli', 'team_id': 2},
            {'username': 'asirin_kuyruk', 'name': 'Kuyruk Personeli', 'team_id': 3},
            {'username': 'asirin_aviyonik', 'name': 'Aviyonik Personeli', 'team_id': 4},
            {'username': 'asirin_montaj', 'name': 'Montaj Personeli', 'team_id': 5},  
        ]

        # Kullanıcıları ve Employee nesnelerini oluşturur
        for user_info in users_info:
            user = User.objects.create_user(
                username=user_info['username'],
                password='asirin',
                email='srnahmet98@gmail.com'
            )

            # Takım ID'ye göre takım bilgisi alır (None ise takım atılmaz)
            team = None
            if user_info['team_id']:
                team = Team.objects.get(id=user_info['team_id'])

            # Employee nesnesini oluştur
            Employee.objects.create(user=user, name=user_info['name'], team=team)

        self.stdout.write(self.style.SUCCESS('Data oluşturma başarılı!'))
