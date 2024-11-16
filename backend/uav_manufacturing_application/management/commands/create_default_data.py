from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from uav_manufacturing_application.models import Employee, Team, PartType, UAVType, UAV, Part
from django.utils.timezone import now

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # IHA Type'ları oluşturma
        uav_types = [
            {'name': 'TB2'},
            {'name': 'TB3'},
            {'name': 'AKINCI'},
            {'name': 'KIZILELMA'}
        ]
        for uav_type in uav_types:
            UAVType.objects.create(**uav_type)

        # IHA oluşturma
        uavs = [
            {'uav_type_id':"1",'create_date':'2024-11-2',},
            {'uav_type_id':"2",'create_date':'2024-11-5'},
            {'uav_type_id':"1",'create_date':'2024-11-7'},
            {'uav_type_id':"3",'create_date':'2024-11-7'},
            {'uav_type_id':"4",'create_date':'2024-11-8'},
            {'uav_type_id':"4",'create_date':'2024-11-8'},
            {'uav_type_id':"4",'create_date':'2024-11-8'},
            {'uav_type_id':"3",'create_date':'2024-11-8'},
            {'uav_type_id':"3",'create_date':'2024-11-10'},
            {'uav_type_id':"2",'create_date':'2024-11-12'},
            {'uav_type_id':"1",'create_date':'2024-11-12'},
            {'uav_type_id':"4",'create_date':'2024-11-16'},
            {'uav_type_id':"2",'create_date':'2024-11-17'},
            {'uav_type_id':"4",'create_date':'2024-11-17'},
        ]
        for uav in uavs:
            UAV.objects.create(**uav)

        # Part Type'ları oluşturma
        part_types = [
            {'name': 'Kanat'},
            {'name': 'Gövde'},
            {'name': 'Kuyruk'},
            {'name': 'Aviyonik'}
        ]
        for part_type in part_types:
            PartType.objects.create(**part_type)

        # Part Type'ları oluşturma
        montagedParts = []
        for index, uav in enumerate(uavs, start=1): 
            for part_type_id in range(1, 5):
                montagedParts.append({
                    'uav_id': index,
                    'uav_type_id': uav['uav_type_id'],
                    'create_date': uav['create_date'],
                    'part_type_id': part_type_id
                })
        for part in montagedParts:
            Part.objects.create(**part)  
        newParts = [
                {'part_type_id': '1', 'uav_type_id': '1', 'create_date': '2024-11-2'},
                {'part_type_id': '3', 'uav_type_id': '4', 'create_date': '2024-11-21'},
                {'part_type_id': '2', 'uav_type_id': '3', 'create_date': '2024-11-5'},
                {'part_type_id': '4', 'uav_type_id': '1', 'create_date': '2024-11-7'},
                {'part_type_id': '3', 'uav_type_id': '2', 'create_date': '2024-11-13'},
                {'part_type_id': '1', 'uav_type_id': '3', 'create_date': '2024-11-9'},
                {'part_type_id': '4', 'uav_type_id': '1', 'create_date': '2024-11-30'},
                {'part_type_id': '2', 'uav_type_id': '4', 'create_date': '2024-11-12'},
                {'part_type_id': '3', 'uav_type_id': '4', 'create_date': '2024-11-6'},
                {'part_type_id': '4', 'uav_type_id': '1', 'create_date': '2024-11-19'},
                {'part_type_id': '2', 'uav_type_id': '3', 'create_date': '2024-11-10'},
                {'part_type_id': '1', 'uav_type_id': '2', 'create_date': '2024-11-27'},
                {'part_type_id': '4', 'uav_type_id': '3', 'create_date': '2024-11-15'},
                {'part_type_id': '2', 'uav_type_id': '4', 'create_date': '2024-11-8'},
                {'part_type_id': '3', 'uav_type_id': '2', 'create_date': '2024-11-14'},
                {'part_type_id': '1', 'uav_type_id': '3', 'create_date': '2024-11-23'},
                {'part_type_id': '2', 'uav_type_id': '4', 'create_date': '2024-11-22'},
                {'part_type_id': '3', 'uav_type_id': '1', 'create_date': '2024-11-17'},
                {'part_type_id': '4', 'uav_type_id': '2', 'create_date': '2024-11-29'},
                {'part_type_id': '1', 'uav_type_id': '4', 'create_date': '2024-11-4'},
                {'part_type_id': '3', 'uav_type_id': '2', 'create_date': '2024-11-24'},
                {'part_type_id': '2', 'uav_type_id': '1', 'create_date': '2024-11-18'},
                {'part_type_id': '4', 'uav_type_id': '3', 'create_date': '2024-11-20'},
                {'part_type_id': '1', 'uav_type_id': '2', 'create_date': '2024-11-16'},
                {'part_type_id': '4', 'uav_type_id': '1', 'create_date': '2024-11-25'},
                {'part_type_id': '3', 'uav_type_id': '2', 'create_date': '2024-11-3'},
                {'part_type_id': '1', 'uav_type_id': '4', 'create_date': '2024-11-28'},
                {'part_type_id': '2', 'uav_type_id': '3', 'create_date': '2024-11-26'},
                {'part_type_id': '4', 'uav_type_id': '1', 'create_date': '2024-11-11'},
                {'part_type_id': '3', 'uav_type_id': '2', 'create_date': '2024-11-1'}
        ]
        for part in newParts:
            Part.objects.create(**part)

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

        # Süper kullanıcıyı oluşturma
        superuser = User.objects.create_superuser(
            username='asirin',
            password='asirin',
            email='srnahmet98@gmail.com'
        )
        Employee.objects.create(user=superuser, name='Admin')

        # Kullanıcı bilgileri
        users_info = [
            {'username': 'asirin_kanat', 'name': 'Kanat Personeli', 'team_id': 1},
            {'username': 'asirin_kanat2', 'name': 'Kanat Personeli 2', 'team_id': 1},
            {'username': 'asirin_kanat3', 'name': 'Kanat Personeli 3', 'team_id': 1},
            {'username': 'asirin_kanat4', 'name': 'Kanat Personeli 4', 'team_id': 1},
            {'username': 'asirin_kanat5', 'name': 'Kanat Personeli 5', 'team_id': 1},
            {'username': 'asirin_kanat6', 'name': 'Kanat Personeli 6', 'team_id': 1},
            {'username': 'asirin_govde', 'name': 'Gövde Personeli ', 'team_id': 2},
            {'username': 'asirin_govde2', 'name': 'Gövde Personeli 2', 'team_id': 2},
            {'username': 'asirin_govde3', 'name': 'Gövde Personeli 3', 'team_id': 2},
            {'username': 'asirin_govde4', 'name': 'Gövde Personeli 4', 'team_id': 2},
            {'username': 'asirin_govde5', 'name': 'Gövde Personeli 5', 'team_id': 2},
            {'username': 'asirin_govde6', 'name': 'Gövde Personeli 6', 'team_id': 2},
            {'username': 'asirin_govde8', 'name': 'Gövde Personeli 8', 'team_id': 2},
            {'username': 'asirin_govde9', 'name': 'Gövde Personeli 9', 'team_id': 2},
            {'username': 'asirin_govde10', 'name': 'Gövde Personeli 10', 'team_id': 2},
            {'username': 'asirin_govde11', 'name': 'Gövde Personeli 11', 'team_id': 2},
            {'username': 'asirin_kuyruk', 'name': 'Kuyruk Personeli', 'team_id': 3},
            {'username': 'asirin_kuyruk2', 'name': 'Kuyruk Personeli 2', 'team_id': 3},
            {'username': 'asirin_kuyruk3', 'name': 'Kuyruk Personeli 3', 'team_id': 3},
            {'username': 'asirin_aviyonik', 'name': 'Aviyonik Personeli', 'team_id': 4},
            {'username': 'asirin_aviyonik2', 'name': 'Aviyonik Personeli 2', 'team_id': 4},
            {'username': 'asirin_aviyonik3', 'name': 'Aviyonik Personeli 3', 'team_id': 4},
            {'username': 'asirin_aviyonik4', 'name': 'Aviyonik Personeli 4', 'team_id': 4},
            {'username': 'asirin_aviyonik5', 'name': 'Aviyonik Personeli 5', 'team_id': 4},
            {'username': 'asirin_montaj', 'name': 'Montaj Personeli', 'team_id': 5}, 
            {'username': 'asirin_montaj2', 'name': 'Montaj Personeli 2', 'team_id': 5},  
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

            # Employee nesnesini oluşturma
            Employee.objects.create(user=user, name=user_info['name'], team=team)

        self.stdout.write(self.style.SUCCESS('Data oluşturma başarılı!'))
