from django.db.models import Q

# from app.login.models import User
# from app.login.models import Department
# from app.login.models import Customer
# from app.login.models import PartItem
# from app.login.models import PartItemResult
# from app.login.models import Configuration

from app.login.models import PartItemResult


class PartItemResultRepository():
    def __init__(self):
        return

    def get_errorcode_by_filter(self, filter):
        q1 = Q()
        q1.connector = 'AND'
        if filter['stage'] != '':
            q1.children.append(('Stage', filter['stage']))
        if filter['fixture'] != '':
            q1.children.append(('FixtureId', filter['fixture']))
        if filter['usn'] != '':
            q1.children.append(('USN', filter['usn']))
        if filter['start_time'] != '':
            start_time = filter['start_time']
        else:
            start_time = '2019-04-01'
        if filter['end_time'] != '':
            end_time = filter['end_time']
        else:
            start_time = '2019-06-01'

        con.add(q1, 'AND')
        return PartItemResult.objects.filter(con, TrnDate__range=(start_time, end_time)).order_by('TrnDate')

