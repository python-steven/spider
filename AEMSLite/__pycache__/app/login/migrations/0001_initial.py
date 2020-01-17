# Generated by Django 2.1.7 on 2019-04-18 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetCodeForm',
            fields=[
                ('Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('DepartmentId', models.IntegerField()),
                ('Department', models.CharField(max_length=10)),
                ('Remark', models.CharField(max_length=10)),
                ('Attachment', models.CharField(max_length=100, null=True)),
                ('BillingType', models.CharField(default=0, max_length=1)),
                ('BudgetCode', models.CharField(max_length=30, null=True)),
                ('ApplyDate', models.DateTimeField()),
                ('ExternalNumberType', models.CharField(max_length=1)),
                ('ExternalNumber', models.CharField(max_length=40, null=True)),
                ('ExternalNumberEffectiveDate', models.DateTimeField(null=True)),
                ('PicId', models.IntegerField(null=True)),
                ('Pic', models.CharField(max_length=20, null=True)),
                ('ProductName', models.CharField(max_length=100)),
                ('Model', models.CharField(max_length=100)),
                ('PurchaseType', models.CharField(max_length=10)),
                ('UnitPrice', models.FloatField()),
                ('Quantity', models.IntegerField()),
                ('Unit', models.CharField(max_length=10)),
                ('Currency', models.CharField(max_length=10)),
                ('CustomerId', models.IntegerField()),
                ('Customer', models.CharField(max_length=50)),
                ('TypeOfMachine', models.CharField(max_length=50)),
                ('ProjectCode', models.CharField(max_length=50)),
                ('ApplyReason', models.CharField(max_length=200)),
                ('SignerId', models.IntegerField()),
                ('Signer', models.CharField(max_length=20)),
                ('Status', models.CharField(max_length=20)),
                ('CreatedTime', models.DateTimeField(auto_now_add=True)),
                ('UpdatedTime', models.DateTimeField()),
                ('OwnerId', models.IntegerField(null=True)),
                ('MergeId', models.BigIntegerField(null=True)),
                ('SignRemarks', models.CharField(max_length=200, null=True)),
                ('AttachmentPath', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'BudgetCodeForm',
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Type', models.CharField(max_length=10)),
                ('Max', models.FloatField()),
                ('Min', models.FloatField()),
                ('Reminders', models.TextField()),
            ],
            options={
                'db_table': 'Configuration',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Customer', models.CharField(max_length=50)),
                ('IsActivated', models.BooleanField(default=True)),
                ('UpdatedTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Department', models.CharField(max_length=50)),
                ('IsActivated', models.BooleanField(default=True)),
                ('UpdatedTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Department',
            },
        ),
        migrations.CreateModel(
            name='MaintenanceLog',
            fields=[
                ('Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('PartItemId', models.CharField(max_length=50)),
                ('PartName', models.CharField(max_length=50)),
                ('UpdatedTime', models.DateTimeField()),
                ('Status', models.CharField(max_length=10)),
                ('Content', models.CharField(max_length=300)),
                ('OperatorId', models.IntegerField()),
                ('CheckDueDate', models.DateTimeField(null=True)),
                ('CheckCount', models.IntegerField(null=True)),
                ('UsedTimes', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'MaintenanceLog',
            },
        ),
        migrations.CreateModel(
            name='PartItem',
            fields=[
                ('Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('USN', models.CharField(max_length=50)),
                ('SN', models.CharField(max_length=20, unique=True)),
                ('OSN', models.CharField(max_length=50)),
                ('PN', models.CharField(max_length=20)),
                ('PartName', models.CharField(max_length=50)),
                ('Spec', models.CharField(max_length=150)),
                ('UsedTimes', models.IntegerField()),
                ('CreatedTime', models.DateTimeField()),
                ('UpdatedTime', models.DateTimeField(auto_now_add=True)),
                ('CheckCycle', models.IntegerField(default=0)),
                ('CheckCycleCount', models.IntegerField(default=0)),
                ('NextCheckCount', models.IntegerField(default=0)),
                ('NextCheckDate', models.DateTimeField(null=True)),
                ('ErrorCounts', models.IntegerField()),
            ],
            options={
                'db_table': 'PartItem',
            },
        ),
        migrations.CreateModel(
            name='PartItemResult',
            fields=[
                ('Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('USN', models.CharField(max_length=50)),
                ('SN', models.CharField(max_length=20)),
                ('OSN', models.CharField(max_length=50)),
                ('Asset', models.CharField(max_length=50, null=True)),
                ('PN', models.CharField(max_length=20)),
                ('PartName', models.CharField(max_length=50)),
                ('Spec', models.CharField(max_length=150)),
                ('UsedTimes', models.IntegerField()),
                ('Stage', models.CharField(max_length=2)),
                ('FixtureId', models.CharField(max_length=10)),
                ('Result', models.CharField(max_length=4)),
                ('ErrorCode', models.CharField(max_length=30)),
                ('TrnDate', models.DateTimeField()),
                ('UpdatedTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'PartItemResult',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EmployeeId', models.CharField(max_length=20)),
                ('Name', models.CharField(max_length=20)),
                ('DepartmentId', models.IntegerField(default=1)),
                ('Password', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=50)),
                ('Role', models.CharField(max_length=20)),
                ('IsActivated', models.BooleanField(default=True)),
                ('CreatedTime', models.DateTimeField()),
                ('UpdatedTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
