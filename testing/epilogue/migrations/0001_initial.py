# Generated by Django 2.0 on 2018-07-20 11:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields.related
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerLevelLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('week', models.IntegerField(default=29)),
                ('year', models.IntegerField(default=2018)),
            ],
            options={
                'db_table': 'erp_customer_level_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityLevelLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lifestyle', models.CharField(max_length=50)),
                ('created', models.DateTimeField(default=datetime.datetime(2018, 7, 20, 17, 10, 58, 464599))),
                ('week', models.IntegerField(default=29)),
                ('year', models.IntegerField(default=2018)),
                ('activated', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'relation_log',
            },
        ),
        migrations.CreateModel(
            name='BusinessCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('business_owner_first_name', models.CharField(max_length=25)),
                ('business_owner_last_name', models.CharField(max_length=25)),
                ('mobile_number', models.CharField(max_length=11)),
                ('created_on', models.DateTimeField()),
                ('signup_completed', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'business_account',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=25)),
                ('last_name', models.CharField(blank=True, max_length=25, null=True)),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('mobile', models.CharField(blank=True, max_length=11, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('w', models.CharField(db_column='weight', default='0.0', max_length=6)),
                ('w_type', models.IntegerField(db_column='weight_type', default=1)),
                ('h', models.CharField(db_column='height', default='0.0', max_length=6)),
                ('h_type', models.IntegerField(db_column='height_type', default=1)),
                ('ls', models.CharField(blank=True, db_column='lifestyle', max_length=50)),
                ('gen', models.CharField(blank=True, db_column='gender', max_length=20, null=True)),
                ('body_type', models.CharField(blank=True, max_length=50)),
                ('food_cat', models.CharField(blank=True, choices=[('veg', 'veg'), ('nonveg', 'nonveg'), ('egg', 'egg')], max_length=50)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('work_pref', models.CharField(blank=True, max_length=10)),
                ('medi_applicable', models.BooleanField(default=False)),
                ('injury_applicable', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'erp_customer',
            },
        ),
        migrations.CreateModel(
            name='CustomerActivityLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('steps', models.IntegerField()),
                ('cals', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('distance', models.IntegerField()),
                ('customer', models.ForeignKey(db_column='customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to='epilogue.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerDietPlanFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(default=0)),
                ('week', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=0)),
                ('followed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilogue.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFoodExclusions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_type', models.CharField(choices=[('lamb_mutton', 'Lamb'), ('seafood', 'Seafood'), ('nuts', 'nuts'), ('wheat', 'wheat'), ('dairy', 'dairy'), ('poultary', 'poultary'), ('egg', 'egg'), ('beef', 'beef'), ('meat', 'meat')], max_length=100)),
                ('customer', models.ForeignKey(db_column='erp_customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='epilogue.Customer')),
            ],
            options={
                'db_table': 'erp_customer_food_exclusion',
            },
        ),
        migrations.CreateModel(
            name='CustomerFoodItemsPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.IntegerField(db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_preference', to='epilogue.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerIsoWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('year', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar', to='epilogue.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMedicalConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_name', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(db_column='erp_customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='epilogue.Customer')),
            ],
            options={
                'db_table': 'erp_customer_medicalcondition',
            },
        ),
        migrations.CreateModel(
            name='CustomerReasons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reasons', to='epilogue.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSleepLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('minutes', models.IntegerField(blank=True)),
                ('saved', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(db_column='erp_customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sleep_logs', to='epilogue.Customer')),
            ],
            options={
                'db_table': 'user_sleep_logs',
            },
        ),
        migrations.CreateModel(
            name='CustomerWaterLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('added', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerWeightRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('weight', models.FloatField()),
                ('weight_type', models.IntegerField()),
                ('customer', models.ForeignKey(db_column='erp_customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='epilogue.Customer')),
            ],
            options={
                'db_table': 'erp_customer_weight_timeline',
            },
        ),
        migrations.CreateModel(
            name='DietFavouriteFoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'item'), (1, 'meal'), (2, 'day')])),
                ('meal', models.IntegerField(choices=[(1, 'Breakfast'), (2, 'Mid Day Snack'), (3, 'Lunch'), (4, 'Evening Snack'), (5, 'Dinner')])),
                ('day', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=0)),
                ('preference', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike'), (0, 'Neutral')], default=0)),
                ('customer_calendar', models.ForeignKey(default=0, on_delete=django.db.models.fields.related.ForeignKey, related_name='favourites', to='epilogue.CustomerIsoWeek')),
            ],
        ),
        migrations.CreateModel(
            name='DishReplacementSuggestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseDietRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_level', models.CharField(max_length=150)),
                ('fit_level', models.CharField(max_length=150)),
                ('new_act_lavel', models.CharField(max_length=150)),
                ('preiodise', models.IntegerField()),
                ('uppercut', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'relation_ep_dp',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('quantity', models.IntegerField(default=0)),
                ('calarie', models.FloatField()),
                ('serving', models.TextField()),
                ('size', models.CharField(max_length=100, null=True)),
                ('weight', models.FloatField()),
                ('fat', models.FloatField()),
                ('protein', models.FloatField()),
                ('carbohydrates', models.FloatField()),
                ('m1', models.IntegerField(default=0)),
                ('m2', models.IntegerField(default=0)),
                ('m3', models.IntegerField(default=0)),
                ('m4', models.IntegerField(default=0)),
                ('m5_loss', models.IntegerField(default=0)),
                ('m5_gain', models.IntegerField(default=0)),
                ('m5_stable', models.IntegerField(default=0)),
                ('fruit', models.IntegerField(default=0)),
                ('drink', models.IntegerField(default=0)),
                ('dairy', models.IntegerField(default=0)),
                ('snaks', models.IntegerField(default=0)),
                ('vegetable', models.IntegerField(default=0)),
                ('grains_cereals', models.IntegerField(default=0)),
                ('cereal_grains', models.IntegerField(default=0)),
                ('salad', models.IntegerField(default=0)),
                ('dessert', models.IntegerField(default=0)),
                ('pulses', models.IntegerField(default=0)),
                ('pulse', models.IntegerField(default=0)),
                ('for_loss', models.IntegerField(default=0)),
                ('wheat', models.IntegerField(default=0)),
                ('lamb_mutton', models.IntegerField(default=0)),
                ('beef', models.IntegerField(default=0)),
                ('seafood', models.IntegerField(default=0)),
                ('poultary', models.IntegerField(default=0)),
                ('meat', models.IntegerField(default=0)),
                ('egg', models.IntegerField(default=0)),
                ('yogurt', models.IntegerField(default=0)),
                ('pork', models.IntegerField(default=0)),
                ('other_meat', models.IntegerField(default=0)),
                ('nut', models.IntegerField(default=0)),
                ('nuts', models.IntegerField(default=0)),
                ('non_veg_gravy_items', models.IntegerField(default=0)),
                ('vegetables', models.IntegerField(default=0)),
                ('cuisine', models.TextField()),
                ('calcium', models.FloatField(default=0)),
                ('vitaminc', models.FloatField(default=0)),
                ('iron', models.FloatField(default=0)),
                ('image_name', models.CharField(max_length=100, null=True)),
                ('squared_diff_weight_loss', models.FloatField(default=0)),
                ('squared_diff_weight_maintain', models.FloatField(default=0)),
                ('squared_diff_weight_gain', models.FloatField(default=0)),
                ('non_veg', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'business_diet_list',
            },
        ),
        migrations.CreateModel(
            name='FoodTypeSizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
                ('weight', models.IntegerField()),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'food_type_sizes',
            },
        ),
        migrations.CreateModel(
            name='GeneratedDietPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user_week_id', models.IntegerField(default=1)),
                ('week_id', models.IntegerField(default=1)),
                ('company_id', models.IntegerField(default=0)),
                ('plan_type', models.CharField(default='system generated plan', max_length=50)),
                ('medi_applicable', models.CharField(default='', max_length=20)),
                ('year', models.IntegerField(default=2018)),
                ('followed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(db_column='erp_customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dietplans', to='epilogue.Customer')),
            ],
            options={
                'db_table': 'erp_diet_plan',
            },
        ),
        migrations.CreateModel(
            name='GeneratedDietPlanFoodDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=255, null=True)),
                ('meal_type', models.CharField(max_length=20, null=True)),
                ('day', models.IntegerField(default=5)),
                ('calorie', models.CharField(default='0', max_length=50)),
                ('weight', models.FloatField(default=0)),
                ('quantity', models.FloatField(default=0)),
                ('food_type', models.CharField(max_length=50, null=True)),
                ('size', models.CharField(max_length=50, null=True)),
                ('dietplan', models.ForeignKey(db_column='erp_diet_plan_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='epilogue.GeneratedDietPlan')),
                ('food_item', models.ForeignKey(db_column='business_diet_list_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='epilogue.Food')),
            ],
            options={
                'db_table': 'erp_diet_plan_food_details',
            },
            managers=[
                ('day1', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='LoginCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('status_id', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('email_confirm', models.CharField(max_length=50)),
                ('customer', models.OneToOneField(db_column='erp_customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='epilogue.Customer')),
            ],
            options={
                'db_table': 'login_customer',
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'glo_objective',
            },
        ),
        migrations.CreateModel(
            name='Reasons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=20, null=True)),
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sku', models.IntegerField(db_index=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='epilogue.Customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WaterContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('bottle', 'Bottle'), ('glass', 'Glass')], max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='dishreplacementsuggestions',
            name='dietplan_food_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggestions', to='epilogue.GeneratedDietPlanFoodDetails'),
        ),
        migrations.AddField(
            model_name='dishreplacementsuggestions',
            name='food',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='epilogue.Food'),
        ),
        migrations.AddField(
            model_name='dietfavouritefoods',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilogue.Food'),
        ),
        migrations.AddField(
            model_name='customerwaterlogs',
            name='container',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='epilogue.WaterContainer'),
        ),
        migrations.AddField(
            model_name='customerwaterlogs',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='water_logs', to='epilogue.Customer'),
        ),
        migrations.AddField(
            model_name='customerreasons',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='epilogue.Reasons'),
        ),
        migrations.AddField(
            model_name='customerfooditemspreference',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epilogue.Food'),
        ),
        migrations.AddField(
            model_name='customer',
            name='objective',
            field=models.ForeignKey(db_column='objective', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='epilogue.Objective'),
        ),
        migrations.AddField(
            model_name='activitylevellog',
            name='customer',
            field=models.ForeignKey(db_column='erp_customer_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activitylevel_logs', to='epilogue.Customer'),
        ),
        migrations.AlterUniqueTogether(
            name='dietfavouritefoods',
            unique_together={('customer_calendar', 'type', 'meal', 'day', 'food')},
        ),
        migrations.AddIndex(
            model_name='customerwaterlogs',
            index=models.Index(fields=['customer_id'], name='epilogue_cu_custome_23b50a_idx'),
        ),
        migrations.AddIndex(
            model_name='customerwaterlogs',
            index=models.Index(fields=['container'], name='epilogue_cu_contain_cebfe3_idx'),
        ),
        migrations.AddIndex(
            model_name='customerisoweek',
            index=models.Index(fields=['customer', '-week', '-year'], name='epilogue_cu_custome_1d8b99_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='customerisoweek',
            unique_together={('customer', 'week', 'year')},
        ),
        migrations.AlterIndexTogether(
            name='customerfooditemspreference',
            index_together={('customer', 'food')},
        ),
        migrations.AddIndex(
            model_name='customerdietplanfollow',
            index=models.Index(fields=['customer', '-day', '-week', '-year'], name='epilogue_cu_custome_d7d8f8_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='customerdietplanfollow',
            unique_together={('customer', 'day', 'week', 'year', 'followed')},
        ),
    ]
