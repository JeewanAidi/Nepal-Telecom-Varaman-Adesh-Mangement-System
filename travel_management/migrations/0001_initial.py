from django.db import migrations, models
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='विभाग')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=20, unique=True, verbose_name='कर्मचारी नं.')),
                ('name', models.CharField(max_length=200, verbose_name='नाम')),
                ('name_nepali', models.CharField(blank=True, max_length=200, null=True, verbose_name='नाम (नेपाली)')),
                ('position', models.CharField(max_length=200, verbose_name='पद')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='फोन')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='इमेल')),
                ('is_active', models.BooleanField(default=True, verbose_name='सक्रिय')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel_management.department', verbose_name='विभाग')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TravelOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(editable=False, max_length=20, unique=True, verbose_name='आदेश नं.')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='मिति')),
                ('travel_location', models.CharField(max_length=500, verbose_name='भ्रमण स्थान')),
                ('purpose', models.TextField(verbose_name='भ्रमणको उद्देश्य')),
                ('from_date', models.DateField(verbose_name='मिति देखि')),
                ('to_date', models.DateField(verbose_name='मिति सम्म')),
                ('transport_type', models.CharField(choices=[('Bus', 'Bus - बस'), ('Jeep', 'Jeep - जीप'), ('Motorcycle', 'Motorcycle - मोटरसाइकल'), ('Car', 'Car - कार'), ('Office Vehicle', 'Office Vehicle - कार्यालय सवारी'), ('Hired Vehicle', 'Hired Vehicle - भाडाको सवारी'), ('Other', 'Other - अन्य')], max_length=50, verbose_name='यातायातको साधन')),
                ('vehicle_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='सवारी नं.')),
                ('work_description', models.TextField(verbose_name='गर्नुपर्ने काम विवरण')),
                ('status', models.CharField(choices=[('Pending', 'Pending - बाँकी'), ('Active', 'Active - सक्रिय'), ('Completed', 'Completed - सम्पन्न'), ('Cancelled', 'Cancelled - रद्द')], default='Pending', max_length=20, verbose_name='स्थिति')),
                ('approved_by', models.CharField(blank=True, max_length=200, null=True, verbose_name='स्वीकृत गर्ने अधिकारी')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='कैफियत')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_management.employee', verbose_name='कर्मचारी')),
            ],
            options={
                'verbose_name': 'Travel Order',
                'verbose_name_plural': 'Travel Orders',
                'ordering': ['-created_at'],
            },
        ),
    ]
